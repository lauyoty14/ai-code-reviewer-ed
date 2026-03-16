"""CLI entry point for the MVP analyzer pipeline."""
from __future__ import annotations

import argparse
from pathlib import Path
import sys


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from analyzer.repo_scanner import clone_repository
from analyzer.tp_detector import detect_tps
from analyzer.file_collector import collect_files
from analyzer.report_builder import build_report


def main() -> int:
    """Run the repository analysis pipeline."""
    parser = argparse.ArgumentParser(description="Run the AI Code Reviewer analyzer.")
    parser.add_argument("repo_url", help="Git repository URL to analyze.")
    args = parser.parse_args()

    repo_url = args.repo_url

    repo_path = clone_repository(repo_url)
    tps = detect_tps(repo_path)
    tp_files = collect_files(repo_path, tps)

    report_path = build_report(repo_url, tp_files, REPO_ROOT / "analysis_report.md")

    print(f"Report written to: {report_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())