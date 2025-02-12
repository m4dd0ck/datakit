"""File and directory utilities."""

import hashlib
import shutil
from pathlib import Path


def find_files(
    directory: str | Path,
    pattern: str = "*",
    recursive: bool = True,
) -> list[Path]:
    """Find files matching a pattern.

    Args:
        directory: Directory to search
        pattern: Glob pattern (e.g., "*.csv", "**/*.json")
        recursive: Search subdirectories

    Returns:
        List of matching file paths
    """
    directory = Path(directory)
    if recursive:
        return list(directory.rglob(pattern))
    return list(directory.glob(pattern))


def ensure_dir(path: str | Path) -> Path:
    """Create directory if it doesn't exist."""
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path


def safe_copy(src: str | Path, dst: str | Path, overwrite: bool = False) -> Path:
    """Copy file with safety checks.

    Args:
        src: Source file
        dst: Destination file or directory
        overwrite: Allow overwriting existing file

    Returns:
        Path to copied file
    """
    src = Path(src)
    dst = Path(dst)

    if not src.exists():
        raise FileNotFoundError(f"Source not found: {src}")

    if dst.is_dir():
        dst = dst / src.name

    if dst.exists() and not overwrite:
        raise FileExistsError(f"Destination exists: {dst}")

    ensure_dir(dst.parent)
    shutil.copy2(src, dst)
    return dst


def safe_move(src: str | Path, dst: str | Path, overwrite: bool = False) -> Path:
    """Move file with safety checks."""
    src = Path(src)
    dst = Path(dst)

    if not src.exists():
        raise FileNotFoundError(f"Source not found: {src}")

    if dst.is_dir():
        dst = dst / src.name

    if dst.exists() and not overwrite:
        raise FileExistsError(f"Destination exists: {dst}")

    ensure_dir(dst.parent)
    shutil.move(src, dst)
    return dst


def file_hash(path: str | Path, algorithm: str = "sha256") -> str:
    """Calculate hash of a file.

    Args:
        path: File path
        algorithm: Hash algorithm (md5, sha1, sha256, etc.)

    Returns:
        Hex digest of file hash
    """
    h = hashlib.new(algorithm)
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def get_file_size(path: str | Path, human_readable: bool = False) -> int | str:
    """Get file size in bytes or human-readable format."""
    size = Path(path).stat().st_size
    if not human_readable:
        return size

    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size < 1024:
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} PB"


def read_text(path: str | Path, encoding: str = "utf-8") -> str:
    """Read entire file as text."""
    return Path(path).read_text(encoding=encoding)


def write_text(path: str | Path, content: str, encoding: str = "utf-8") -> None:
    """Write text to file, creating parent dirs if needed."""
    path = Path(path)
    ensure_dir(path.parent)
    path.write_text(content, encoding=encoding)
