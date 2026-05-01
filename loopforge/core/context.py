"""
Context: reads codebase files and builds context dict for agents.
"""

from pathlib import Path

IGNORE_DIRS = {".git", "__pycache__", "node_modules", ".venv", "venv", ".mypy_cache", ".ruff_cache", "dist", "build"}
INCLUDE_EXTENSIONS = {".py", ".ts", ".js", ".tsx", ".jsx", ".go", ".rs", ".yaml", ".yml", ".toml", ".md", ".txt"}
MAX_FILE_SIZE_BYTES = 200_000  # Skip files larger than 200KB


def read_codebase(target: Path) -> dict:
    """
    Read a directory or single file into a context dict.

    Returns:
        {
            "content": str,        # Concatenated file contents with headers
            "summary": str,        # Short summary for planning prompts
            "file_count": int,
            "token_estimate": int, # Rough estimate (chars / 4)
        }
    """
    if target.is_file():
        files = [target]
    else:
        files = _collect_files(target)

    parts = []
    for path in files:
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
            if len(text) > MAX_FILE_SIZE_BYTES:
                text = text[:MAX_FILE_SIZE_BYTES] + "\n... [truncated]"
            parts.append(f"### FILE: {path}\n```\n{text}\n```\n")
        except Exception:
            continue

    content = "\n".join(parts)
    token_estimate = len(content) // 4

    summary_lines = [f"- {p}" for p in files[:20]]
    if len(files) > 20:
        summary_lines.append(f"  ... and {len(files) - 20} more files")

    return {
        "content": content,
        "summary": "\n".join(summary_lines),
        "file_count": len(files),
        "token_estimate": token_estimate,
    }


def _collect_files(root: Path) -> list[Path]:
    results = []
    for path in sorted(root.rglob("*")):
        if any(part in IGNORE_DIRS for part in path.parts):
            continue
        if path.is_file() and path.suffix in INCLUDE_EXTENSIONS:
            results.append(path)
    return results
