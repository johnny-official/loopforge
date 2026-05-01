"""
DocAgent — reads finalized code and generates technical specs, usage docs,
and legal-technical summaries.
"""

from pathlib import Path
from typing import Any

from loopforge.core.context import read_codebase
from loopforge.utils.logger import get_logger
from loopforge.utils.model_client import ModelClient

logger = get_logger(__name__)


class DocAgent:
    def __init__(self, config: dict):
        self.config = config
        self.model = ModelClient(model=config["models"]["doc_agent"])

    def run(
        self,
        target: Path,
        output_dir: Path,
        code_context: dict | None = None,
    ) -> dict[str, Any]:
        logger.info(f"DocAgent starting | target={target}")

        context = code_context or read_codebase(target)
        output_dir.mkdir(parents=True, exist_ok=True)

        results = {}

        # Generate technical spec
        spec = self._generate_spec(context)
        spec_path = output_dir / "SPEC.md"
        spec_path.write_text(spec)
        results["spec"] = str(spec_path)
        logger.info(f"Spec written to {spec_path}")

        # Generate usage documentation
        usage = self._generate_usage(context)
        usage_path = output_dir / "USAGE.md"
        usage_path.write_text(usage)
        results["usage"] = str(usage_path)
        logger.info(f"Usage doc written to {usage_path}")

        return {
            "status": "success",
            "outputs": results,
            "summary": f"Generated {len(results)} documents in {output_dir}",
        }

    def _generate_spec(self, context: dict) -> str:
        prompt = f"""You are a senior technical writer. Generate a detailed technical specification document for this codebase.

Include:
1. Overview and purpose
2. Architecture description
3. Key modules and their responsibilities
4. Data flows
5. Configuration options
6. Known limitations

CODEBASE:
{context['content']}

Output clean Markdown.
"""
        return self.model.complete(prompt)

    def _generate_usage(self, context: dict) -> str:
        prompt = f"""You are a senior technical writer. Generate a practical usage guide for this codebase.

Include:
1. Installation
2. Quick start
3. CLI reference (all flags and options)
4. Example commands for common tasks
5. Configuration guide
6. Troubleshooting

CODEBASE:
{context['content']}

Output clean Markdown.
"""
        return self.model.complete(prompt)

    def _generate_legal_summary(self, context: dict) -> str:
        """
        Generate a structured legal-technical summary.
        Used when code is the subject of a legal agreement or technical review.
        """
        prompt = f"""You are acting as a technical expert assisting legal review.
Analyze this codebase and produce a structured technical summary suitable for legal documentation.

Include:
1. System purpose and capabilities (plain language)
2. Data processed (types, sensitivity)
3. External dependencies and third-party services
4. Security model overview
5. Potential liability-relevant behaviors (e.g., automated decisions, data retention)
6. Ambiguous or under-specified behaviors that may require contractual clarification

CODEBASE:
{context['content']}

Output structured Markdown with clear section headers.
"""
        return self.model.complete(prompt)
