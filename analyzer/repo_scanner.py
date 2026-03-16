"""Repository cloning utilities."""
from __future__ import annotations

from pathlib import Path
import tempfile

from git import Repo


def clone_repository(repo_url: str, destination: str | Path | None = None) -> Path:
    """Clone a repository to a local path.

    Args:
        repo_url: URL of the Git repository to clone.
        destination: Optional directory to clone into. If None, a temporary
            directory is created.

    Returns:
        Path to the cloned repository root.

    Raises:
        ValueError: If repo_url is empty.
        git.exc.GitError: If cloning fails.
    """
    if not repo_url or not repo_url.strip():
        raise ValueError("repo_url must be a non-empty string.")

    if destination is None:
        destination_path = Path(tempfile.mkdtemp(prefix="ai-code-reviewer-ed-"))
    else:
        destination_path = Path(destination)
        destination_path.mkdir(parents=True, exist_ok=True)

    Repo.clone_from(repo_url, destination_path)
    return destination_path