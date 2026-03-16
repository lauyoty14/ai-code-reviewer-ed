"""Assignment (TP) detection utilities."""
from __future__ import annotations

from pathlib import Path
import os
import re


_TP_FILE_PATTERN = re.compile(r"^tp-(\d+)\.hs$", re.IGNORECASE)
_TP_DIR_PATTERN = re.compile(r"^tp-(\d+)$", re.IGNORECASE)


def detect_tps(repo_path: str | Path) -> list[str]:
    """Detect assignment identifiers within a repository.

    Looks for files named like tp-<n>.hs and directories named tp-<n>.

    Args:
        repo_path: Path to the cloned repository.

    Returns:
        A sorted list of detected assignment identifiers (e.g., ["tp1", "tp2"]).
    """
    root = Path(repo_path)
    if not root.exists():
        raise FileNotFoundError(f"Repository path does not exist: {root}")

    tp_numbers: set[int] = set()

    for dirpath, dirnames, filenames in os.walk(root):
        _filter_dirs_in_place(dirnames)

        for dirname in dirnames:
            match = _TP_DIR_PATTERN.match(dirname)
            if match:
                tp_numbers.add(int(match.group(1)))

        for filename in filenames:
            match = _TP_FILE_PATTERN.match(filename)
            if match:
                tp_numbers.add(int(match.group(1)))

    return [f"tp{num}" for num in sorted(tp_numbers)]


def _filter_dirs_in_place(dirnames: list[str]) -> None:
    """Filter out directories we should skip during walks."""
    ignored = {".git"}
    dirnames[:] = [d for d in dirnames if d not in ignored]