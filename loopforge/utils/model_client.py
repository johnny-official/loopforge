"""
ModelClient: thin abstraction over LLM API backends.
Supports: Anthropic Claude, Xiaomi MiMo (OpenAI-compatible endpoint).
"""

import json
import os
from typing import Any

from loopforge.utils.logger import get_logger

logger = get_logger(__name__)


class ModelClient:
    """
    Unified client for Claude and MiMo APIs.

    MiMo uses an OpenAI-compatible endpoint, so we use the openai SDK
    pointed at platform.xiaomimimo.com when a MiMo model is configured.
    """

    CLAUDE_MODELS = {"claude-sonnet-4-5", "claude-opus-4", "claude-haiku-4-5-20251001"}
    MIMO_BASE_URL = "https://api.xiaomimimo.com/v1"

    def __init__(self, model: str):
        self.model = model
        self.backend = self._detect_backend(model)
        self._client = None

    def _detect_backend(self, model: str) -> str:
        if any(model.startswith(m) for m in ("claude",)):
            return "anthropic"
        if "mimo" in model.lower():
            return "mimo"
        return "anthropic"  # default

    def _get_client(self):
        if self._client:
            return self._client

        if self.backend == "anthropic":
            import anthropic
            self._client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
        elif self.backend == "mimo":
            import openai
            self._client = openai.OpenAI(
                api_key=os.environ["MIMO_API_KEY"],
                base_url=self.MIMO_BASE_URL,
            )
        return self._client

    def complete(self, prompt: str, max_tokens: int = 8192) -> str:
        client = self._get_client()
        logger.debug(f"Calling {self.backend} | model={self.model} | prompt_len={len(prompt)}")

        if self.backend == "anthropic":
            response = client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                messages=[{"role": "user", "content": prompt}],
            )
            return response.content[0].text

        elif self.backend == "mimo":
            response = client.chat.completions.create(
                model=self.model,
                max_tokens=max_tokens,
                messages=[{"role": "user", "content": prompt}],
            )
            return response.choices[0].message.content

        raise ValueError(f"Unknown backend: {self.backend}")

    def parse_json(self, text: str) -> Any:
        """Extract and parse JSON from model response."""
        text = text.strip()
        # Strip markdown code fences if present
        if text.startswith("```"):
            lines = text.split("\n")
            text = "\n".join(lines[1:-1])
        try:
            return json.loads(text)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {e}\nRaw: {text[:500]}")
            return {}
