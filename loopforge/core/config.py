"""
Config loader — reads models.yaml and merges with defaults.
"""

from pathlib import Path
import yaml

DEFAULTS = {
    "models": {
        "coordinator": "claude-sonnet-4-5",
        "code_agent": "claude-sonnet-4-5",
        "doc_agent": "claude-sonnet-4-5",
        "synthesis": "claude-sonnet-4-5",
    },
    "max_iterations": 8,
    "max_context_tokens": 180_000,
    "test_command": "pytest",
    "lint_command": "ruff check .",
    "dry_run": False,
    "verbose": False,
}


def load_config(config_path: Path) -> dict:
    config = DEFAULTS.copy()

    if config_path.exists():
        with open(config_path) as f:
            user_config = yaml.safe_load(f) or {}
        _deep_merge(config, user_config)
    else:
        pass  # Use defaults silently

    return config


def _deep_merge(base: dict, override: dict) -> None:
    for key, value in override.items():
        if key in base and isinstance(base[key], dict) and isinstance(value, dict):
            _deep_merge(base[key], value)
        else:
            base[key] = value
