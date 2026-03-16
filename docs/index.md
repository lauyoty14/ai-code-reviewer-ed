# AI Code Reviewer - Estructuras de Datos

AI Code Reviewer is a lightweight analyzer designed to help collaborators review student code faster.
It scans GitHub repositories from a university course, detects assignments (TPs), collects relevant
source files, and generates a structured Markdown report.

## How It Works

1. Clone the student's repository.
2. Detect assignment identifiers (e.g., tp-1.hs or tp-3/).
3. Collect relevant Haskell and C++ source files.
4. Generate a report summarizing detected TPs, files, and languages.

This MVP does not include AI analysis yet. It focuses on providing a reliable, repeatable pipeline
that runs locally or in GitHub Actions.