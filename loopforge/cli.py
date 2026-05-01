#!/usr/bin/env python3
"""
LoopForge CLI — Agentic closed-loop development pipeline.
"""

import argparse
import sys
from pathlib import Path

from loopforge.core.pipeline import Pipeline
from loopforge.core.config import load_config
from loopforge.utils.logger import get_logger

logger = get_logger(__name__)


def parse_args():
    parser = argparse.ArgumentParser(
        prog="loopforge",
        description="Agentic closed-loop coding and documentation pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  loopforge --mode code --target ./src --task "refactor auth module"
  loopforge --mode full --target ./src --task "add rate limiting" --doc-output ./docs
  loopforge --mode doc  --target ./src --output ./docs/spec.md
        """,
    )

    parser.add_argument(
        "--mode",
        choices=["code", "doc", "full"],
        required=True,
        help="Pipeline mode: code-only, doc-only, or full (code + docs)",
    )
    parser.add_argument(
        "--target",
        type=Path,
        required=True,
        help="Path to codebase directory or file",
    )
    parser.add_argument(
        "--task",
        type=str,
        required=True,
        help="Task description for the agent",
    )
    parser.add_argument(
        "--doc-output",
        type=Path,
        default=Path("./docs"),
        help="Output directory for generated documentation (default: ./docs)",
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=Path("config/models.yaml"),
        help="Path to model config file (default: config/models.yaml)",
    )
    parser.add_argument(
        "--max-iterations",
        type=int,
        default=8,
        help="Max self-correction iterations before surfacing to user (default: 8)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Plan and display steps without executing",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Verbose logging",
    )

    return parser.parse_args()


def main():
    args = parse_args()

    if not args.target.exists():
        logger.error(f"Target path does not exist: {args.target}")
        sys.exit(1)

    config = load_config(args.config)
    config["max_iterations"] = args.max_iterations
    config["dry_run"] = args.dry_run
    config["verbose"] = args.verbose

    logger.info(f"LoopForge starting | mode={args.mode} | target={args.target}")
    logger.info(f"Task: {args.task}")

    pipeline = Pipeline(config=config)

    try:
        result = pipeline.run(
            mode=args.mode,
            target=args.target,
            task=args.task,
            doc_output=args.doc_output,
        )
        logger.info(f"Pipeline complete | status={result['status']}")
        if result.get("summary"):
            print("\n" + "=" * 60)
            print(result["summary"])
            print("=" * 60)
    except KeyboardInterrupt:
        logger.warning("Interrupted by user.")
        sys.exit(130)
    except Exception as e:
        logger.error(f"Pipeline failed: {e}")
        if args.verbose:
            raise
        sys.exit(1)


if __name__ == "__main__":
    main()
