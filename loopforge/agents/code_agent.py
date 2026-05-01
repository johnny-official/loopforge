"""
CodeAgent — reads codebase, implements task, runs lint/tests, self-corrects.

Loop:
    Read context → Plan → Implement → Lint/Test → Self-correct (on failure)
    Max iterations configurable (default: 8)
"""

import subprocess
from pathlib import Path
from typing import Any

from loopforge.core.context import read_codebase
from loopforge.utils.logger import get_logger
from loopforge.utils.model_client import ModelClient

logger = get_logger(__name__)


class CodeAgent:
    def __init__(self, config: dict):
        self.config = config
        self.max_iterations = config.get("max_iterations", 8)
        self.model = ModelClient(model=config["models"]["code_agent"])
        self.dry_run = config.get("dry_run", False)

    def run(self, target: Path, task: str) -> dict[str, Any]:
        logger.info(f"CodeAgent starting | target={target}")

        # Step 1: Read codebase context
        context = read_codebase(target)
        logger.info(f"Context loaded | files={context['file_count']} | tokens≈{context['token_estimate']}")

        # Step 2: Plan
        plan = self._plan(context=context, task=task)
        logger.info(f"Plan generated | steps={len(plan['steps'])}")

        if self.dry_run:
            return {"status": "dry_run", "plan": plan, "summary": self._format_plan(plan)}

        # Step 3: Closed loop — implement → validate → fix
        iteration = 0
        last_error = None

        while iteration < self.max_iterations:
            iteration += 1
            logger.info(f"Iteration {iteration}/{self.max_iterations}")

            # Implement
            patch = self._implement(context=context, task=task, plan=plan, error=last_error)
            self._apply_patch(patch)

            # Validate
            lint_result = self._run_lint()
            test_result = self._run_tests()

            if lint_result["passed"] and test_result["passed"]:
                logger.info(f"✓ All checks passed on iteration {iteration}")
                return {
                    "status": "success",
                    "iterations": iteration,
                    "summary": self._format_success(iteration, task),
                    "patch": patch,
                }

            # Collect errors for next iteration
            last_error = {
                "lint": lint_result.get("output", ""),
                "tests": test_result.get("output", ""),
            }
            logger.warning(f"Checks failed | lint_ok={lint_result['passed']} | tests_ok={test_result['passed']}")

        # Exhausted iterations
        logger.error(f"Max iterations ({self.max_iterations}) reached without passing checks.")
        return {
            "status": "failed",
            "iterations": iteration,
            "last_error": last_error,
            "summary": self._format_failure(last_error),
        }

    def _plan(self, context: dict, task: str) -> dict:
        prompt = f"""You are a senior software engineer. Given this codebase context and task, produce a step-by-step implementation plan.

TASK: {task}

CODEBASE SUMMARY:
{context['summary']}

Respond as JSON: {{"steps": ["step1", "step2", ...], "files_to_modify": ["path1", ...]}}
"""
        response = self.model.complete(prompt)
        return self.model.parse_json(response)

    def _implement(self, context: dict, task: str, plan: dict, error: dict | None) -> dict:
        error_section = ""
        if error:
            error_section = f"""
PREVIOUS ATTEMPT FAILED. Fix these errors specifically:
LINT: {error['lint']}
TESTS: {error['tests']}
"""
        prompt = f"""You are a senior software engineer implementing a code change.

TASK: {task}
PLAN: {plan}
{error_section}
CODEBASE:
{context['content']}

Generate a unified diff patch to implement the task. Respond as JSON:
{{"patches": [{{"file": "path/to/file.py", "diff": "unified diff content"}}]}}
"""
        response = self.model.complete(prompt)
        return self.model.parse_json(response)

    def _apply_patch(self, patch: dict) -> None:
        if not patch.get("patches"):
            logger.warning("No patches to apply.")
            return
        for p in patch["patches"]:
            logger.info(f"Applying patch to {p['file']}")
            # In production: apply unified diff via `patch` CLI or difflib
            # Placeholder for actual patch application
            pass

    def _run_lint(self) -> dict:
        cmd = self.config.get("lint_command", "ruff check .")
        try:
            result = subprocess.run(cmd.split(), capture_output=True, text=True, timeout=60)
            passed = result.returncode == 0
            return {"passed": passed, "output": result.stdout + result.stderr}
        except Exception as e:
            return {"passed": False, "output": str(e)}

    def _run_tests(self) -> dict:
        cmd = self.config.get("test_command", "pytest")
        try:
            result = subprocess.run(cmd.split(), capture_output=True, text=True, timeout=120)
            passed = result.returncode == 0
            return {"passed": passed, "output": result.stdout + result.stderr}
        except Exception as e:
            return {"passed": False, "output": str(e)}

    def _format_plan(self, plan: dict) -> str:
        lines = ["[DRY RUN] Implementation plan:"]
        for i, step in enumerate(plan.get("steps", []), 1):
            lines.append(f"  {i}. {step}")
        return "\n".join(lines)

    def _format_success(self, iterations: int, task: str) -> str:
        return f"✓ Task complete in {iterations} iteration(s): {task}"

    def _format_failure(self, error: dict) -> str:
        return f"✗ Could not complete task after {self.max_iterations} iterations.\nLast errors:\n{error}"
