"""Zip file utilities."""

import zipfile
from pathlib import Path
from typing import Callable


def create_zip(
    output_path: str | Path,
    files: list[str | Path] | None = None,
    directory: str | Path | None = None,
    compression: int = zipfile.ZIP_DEFLATED,
) -> Path:
    """Create a zip file from files or directory.

    Args:
        output_path: Path for the output zip file
        files: List of files to include
        directory: Directory to zip (alternative to files)
        compression: Compression type

    Returns:
        Path to created zip file
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(output_path, "w", compression) as zf:
        if directory:
            directory = Path(directory)
            for file in directory.rglob("*"):
                if file.is_file():
                    arcname = file.relative_to(directory)
                    zf.write(file, arcname)

        if files:
            for file in files:
                file = Path(file)
                zf.write(file, file.name)

    return output_path


def extract_zip(
    zip_path: str | Path,
    output_dir: str | Path,
    members: list[str] | None = None,
) -> Path:
    """Extract zip file contents.

    Args:
        zip_path: Path to zip file
        output_dir: Directory to extract to
        members: Specific files to extract (all if None)

    Returns:
        Path to extraction directory
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(zip_path, "r") as zf:
        if members:
            for member in members:
                zf.extract(member, output_dir)
        else:
            zf.extractall(output_dir)

    return output_dir


def list_zip_contents(zip_path: str | Path) -> list[dict]:
    """List contents of a zip file.

    Args:
        zip_path: Path to zip file

    Returns:
        List of dicts with file info
    """
    result = []
    with zipfile.ZipFile(zip_path, "r") as zf:
        for info in zf.infolist():
            result.append({
                "filename": info.filename,
                "size": info.file_size,
                "compressed_size": info.compress_size,
                "is_dir": info.is_dir(),
            })
    return result


def read_from_zip(zip_path: str | Path, filename: str, encoding: str = "utf-8") -> str:
    """Read a file from within a zip without extracting.

    Args:
        zip_path: Path to zip file
        filename: Name of file inside zip
        encoding: Text encoding

    Returns:
        File contents as string
    """
    with zipfile.ZipFile(zip_path, "r") as zf:
        return zf.read(filename).decode(encoding)


def add_to_zip(
    zip_path: str | Path,
    file_path: str | Path,
    arcname: str | None = None,
) -> None:
    """Add a file to an existing zip.

    Args:
        zip_path: Path to zip file
        file_path: File to add
        arcname: Name inside zip (defaults to file name)
    """
    file_path = Path(file_path)
    if arcname is None:
        arcname = file_path.name

    with zipfile.ZipFile(zip_path, "a") as zf:
        zf.write(file_path, arcname)


def is_valid_zip(zip_path: str | Path) -> bool:
    """Check if file is a valid zip."""
    try:
        with zipfile.ZipFile(zip_path, "r") as zf:
            return zf.testzip() is None
    except (zipfile.BadZipFile, FileNotFoundError):
        return False
