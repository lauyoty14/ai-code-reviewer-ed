"""Report generation utilities."""
from __future__ import annotations

from pathlib import Path


_HASKELL_EXTENSIONS = {".hs"}
_CPP_EXTENSIONS = {".cpp", ".hpp", ".h"}


def build_report(
    repo_url: str,
    tp_files: dict[str, list[str]],
    output_path: str | Path = "analysis_report.md",
) -> Path:
    """Build and save a Markdown analysis report.

    Args:
        repo_url: URL of the analyzed repository.
        tp_files: Mapping of TP identifiers to relative file paths.
        output_path: Where to write the report.

    Returns:
        The path to the generated report.
    """
    output = Path(output_path)

    tp_list = _sorted_tps(list(tp_files.keys()))
    all_files = [path for files in tp_files.values() for path in files]

    haskell_files = sorted({f for f in all_files if _has_extension(f, _HASKELL_EXTENSIONS)})
    cpp_files = sorted({f for f in all_files if _has_extension(f, _CPP_EXTENSIONS)})

    languages = []
    if haskell_files:
        languages.append("Haskell")
    if cpp_files:
        languages.append("C++")

    lines: list[str] = []
    lines.append("# AI Code Reviewer Report")
    lines.append("")
    lines.append(f"Repository: {repo_url}")
    lines.append("")

    lines.append("Detected TPs:")
    lines.extend(_format_list(tp_list))
    lines.append("")

    lines.append("Languages Detected:")
    lines.extend(_format_list(languages))
    lines.append("")

    lines.append("Haskell Files:")
    lines.extend(_format_list(haskell_files))
    lines.append("")

    lines.append("C++ Files:")
    lines.extend(_format_list(cpp_files))
    lines.append("")

    output.write_text("\n".join(lines), encoding="utf-8")
    return output


def _sorted_tps(tps: list[str]) -> list[str]:
    def _tp_key(tp: str) -> tuple[int, str]:
        suffix = "".join(ch for ch in tp if ch.isdigit())
        return (int(suffix) if suffix.isdigit() else 0, tp)

    return sorted(tps, key=_tp_key)


def _format_list(items: list[str]) -> list[str]:
    if not items:
        return ["- None"]
    return [f"- {item}" for item in items]


def _has_extension(path_str: str, extensions: set[str]) -> bool:
    return Path(path_str).suffix.lower() in extensions