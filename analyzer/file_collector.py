"""Assignment file collection utilities."""
from __future__ import annotations

from pathlib import Path
import os
import re


_SUPPORTED_EXTENSIONS = {".hs", ".cpp", ".hpp", ".h"}
_TP_FILE_PATTERN = re.compile(r"^tp-(\d+)\.[a-z0-9]+$", re.IGNORECASE)
_TP_DIR_PATTERN = re.compile(r"^tp-(\d+)$", re.IGNORECASE)


def collect_files(repo_path: str | Path, tps: list[str]) -> dict[str, list[str]]:
    """Collect relevant files for detected assignments.

    Args:
        repo_path: Path to the cloned repository.
        tps: List of detected assignments (e.g., ["tp1", "tp2"]).

    Returns:
        Mapping of assignment identifier to a list of relative file paths.
    """
    root = Path(repo_path)
    if not root.exists():
        raise FileNotFoundError(f"Repository path does not exist: {root}")

    results: dict[str, list[str]] = {tp: [] for tp in tps}
    if not tps:
        return results

    for dirpath, dirnames, filenames in os.walk(root):
        _filter_dirs_in_place(dirnames)
        current_dir = Path(dirpath)

        for filename in filenames:
            if Path(filename).suffix.lower() not in _SUPPORTED_EXTENSIONS:
                continue

            file_path = current_dir / filename
            rel_path = file_path.relative_to(root).as_posix()

            matched_numbers = set()

            file_match = _TP_FILE_PATTERN.match(filename)
            if file_match:
                matched_numbers.add(file_match.group(1))

            for part in file_path.parts:
                dir_match = _TP_DIR_PATTERN.match(part)
                if dir_match:
                    matched_numbers.add(dir_match.group(1))

            for number in matched_numbers:
                tp_key = f"tp{int(number)}"
                if tp_key in results:
                    results[tp_key].append(rel_path)

    for tp_key, files in results.items():
        unique_files = sorted(set(files))
        results[tp_key] = unique_files

    return results


def _filter_dirs_in_place(dirnames: list[str]) -> None:
    """Filter out directories we should skip during walks."""
    ignored = {".git"}
    dirnames[:] = [d for d in dirnames if d not in ignored]