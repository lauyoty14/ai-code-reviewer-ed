# AI Code Reviewer - Estructuras de Datos

AI Code Reviewer is a lightweight analyzer that helps collaborators review student code faster.
It scans a GitHub repository, detects assignment (TP) artifacts, collects relevant source files,
and generates a structured Markdown report. This is an MVP pipeline only; it does not include AI
analysis yet.

## Architecture Overview

- `analyzer/repo_scanner.py`: clones the target repository with GitPython.
- `analyzer/tp_detector.py`: finds assignments based on file and folder patterns.
- `analyzer/file_collector.py`: gathers relevant Haskell and C++ source files.
- `analyzer/report_builder.py`: creates the Markdown report.
- `scripts/run_analysis.py`: CLI entry point that runs the full pipeline.

## Run Locally

1. Install dependencies:

```bash
python -m venv .venv
. .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

2. Run the analyzer:

```bash
python scripts/run_analysis.py <repo_url>
```

The report is saved as `analysis_report.md` in the repository root.

## GitHub Action

A workflow at `.github/workflows/test-analyzer.yml` runs on every pull request. It:

1. Checks out this repository.
2. Installs Python and dependencies.
3. Runs the analyzer against the current repository URL.

This validates the pipeline in CI and keeps the MVP behavior consistent with local runs.