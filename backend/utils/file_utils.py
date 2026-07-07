"""
utils/file_utils.py – shared file-handling utilities
"""
from __future__ import annotations
import os
import uuid
from pathlib import Path
from datetime import datetime, timedelta


def safe_filename(name: str, extension: str = "") -> str:
    """Return a filesystem-safe filename, preserving extension."""
    safe = "".join(c if c.isalnum() or c in "-_." else "_" for c in name)
    if extension and not safe.endswith(extension):
        safe = f"{safe}{extension}"
    return safe


def unique_path(directory: str | Path, prefix: str, extension: str) -> Path:
    """Generate a unique file path using a UUID fragment."""
    uid = str(uuid.uuid4())[:8]
    ts = datetime.now().strftime("%Y%m%d")
    fname = f"{prefix}_{ts}_{uid}{extension}"
    return Path(directory) / fname


def ensure_dir(path: str | Path) -> Path:
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p


def cleanup_old_files(directory: str | Path, max_age_hours: int = 24) -> int:
    """Delete files older than max_age_hours. Returns count deleted."""
    cutoff = datetime.now() - timedelta(hours=max_age_hours)
    deleted = 0
    for f in Path(directory).iterdir():
        if f.is_file():
            mtime = datetime.fromtimestamp(f.stat().st_mtime)
            if mtime < cutoff:
                f.unlink(missing_ok=True)
                deleted += 1
    return deleted


def file_size_mb(path: str | Path) -> float:
    return Path(path).stat().st_size / (1024 * 1024)
