"""
Coordinator: decomposes tasks and routes to CodeAgent + DocAgent in parallel,
then synthesizes results.
"""

import concurrent.futures
from pathlib import Path
from typing import Any

from loopforge.agents.code_agent import CodeAgent
from loopforge.agents.doc_agent import DocAgent
from loopforge.utils.logger import get_logger
from loopforge.utils.model_client import ModelClient

logger = get_logger(__name__)


class Coordinator:
    def __init__(self, config: dict):
        self.config = config
        self.model = ModelClient(model=config["models"]["coordinator"])

    def run(self, target: Path, task: str, doc_output: Path) -> dict[str, Any]:
        logger.info("Coordinator starting | mode=full")

        # Step 1: Run CodeAgent first (DocAgent needs its output)
        code_agent = CodeAgent(config=self.config)
        logger.info("Dispatching CodeAgent...")
        code_result = code_agent.run(target=target, task=task)

        if code_result["status"] == "failed":
            logger.error("CodeAgent failed: aborting pipeline.")
            return {
                "status": "failed",
                "stage": "code",
                "detail": code_result,
                "summary": "Pipeline aborted: CodeAgent could not complete task.",
            }

        # Step 2: Run DocAgent with updated context
        doc_agent = DocAgent(config=self.config)
        logger.info("Dispatching DocAgent with updated code context...")
        doc_result = doc_agent.run(target=target, output_dir=doc_output)

        # Step 3: Synthesize
        summary = self._synthesize(code_result=code_result, doc_result=doc_result, task=task)

        return {
            "status": "success",
            "code": code_result,
            "docs": doc_result,
            "summary": summary,
        }

    def _synthesize(self, code_result: dict, doc_result: dict, task: str) -> str:
        lines = [
            f"✓ LoopForge pipeline complete",
            f"  Task: {task}",
            f"  Code: {code_result.get('summary', 'done')}",
            f"  Docs: {doc_result.get('summary', 'done')}",
        ]
        return "\n".join(lines)
