"""Basic tests for LoopForge core modules."""

from pathlib import Path
import pytest
from loopforge.core.config import load_config
from loopforge.core.context import read_codebase, _collect_files


def test_load_config_defaults():
    config = load_config(Path("nonexistent.yaml"))
    assert config["max_iterations"] == 8
    assert "models" in config
    assert "code_agent" in config["models"]


def test_read_codebase_single_file(tmp_path):
    f = tmp_path / "sample.py"
    f.write_text("def hello(): return 'world'")
    ctx = read_codebase(f)
    assert ctx["file_count"] == 1
    assert "hello" in ctx["content"]
    assert ctx["token_estimate"] > 0


def test_read_codebase_directory(tmp_path):
    (tmp_path / "a.py").write_text("x = 1")
    (tmp_path / "b.py").write_text("y = 2")
    (tmp_path / "__pycache__").mkdir()
    (tmp_path / "__pycache__" / "skip.pyc").write_text("junk")

    ctx = read_codebase(tmp_path)
    assert ctx["file_count"] == 2  # __pycache__ skipped


def test_collect_files_ignores_hidden(tmp_path):
    (tmp_path / "main.py").write_text("pass")
    (tmp_path / ".git").mkdir()
    (tmp_path / ".git" / "config").write_text("git stuff")

    files = _collect_files(tmp_path)
    paths = [str(f) for f in files]
    assert all(".git" not in p for p in paths)
