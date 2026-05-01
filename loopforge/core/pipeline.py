"""
Pipeline — orchestrates agent execution for code, doc, and full modes.
"""

from pathlib import Path
from typing import Any

from loopforge.agents.code_agent import CodeAgent
from loopforge.agents.doc_agent import DocAgent
from loopforge.agents.coordinator import Coordinator
from loopforge.utils.logger import get_logger

logger = get_logger(__name__)


class Pipeline:
    """
    Top-level pipeline orchestrator.

    Modes:
        code  — Run CodeAgent only (closed-loop refactor/implement)
        doc   — Run DocAgent only (generate docs from existing code)
        full  — Run Coordinator (CodeAgent + DocAgent in parallel, then Synthesis)
    """

    def __init__(self, config: dict):
        self.config = config

    def run(
        self,
        mode: str,
        target: Path,
        task: str,
        doc_output: Path,
    ) -> dict[str, Any]:

        if mode == "code":
            return self._run_code(target, task)
        elif mode == "doc":
            return self._run_doc(target, doc_output)
        elif mode == "full":
            return self._run_full(target, task, doc_output)
        else:
            raise ValueError(f"Unknown mode: {mode}")

    def _run_code(self, target: Path, task: str) -> dict:
        agent = CodeAgent(config=self.config)
        return agent.run(target=target, task=task)

    def _run_doc(self, target: Path, doc_output: Path) -> dict:
        agent = DocAgent(config=self.config)
        return agent.run(target=target, output_dir=doc_output)

    def _run_full(self, target: Path, task: str, doc_output: Path) -> dict:
        coordinator = Coordinator(config=self.config)
        return coordinator.run(target=target, task=task, doc_output=doc_output)
