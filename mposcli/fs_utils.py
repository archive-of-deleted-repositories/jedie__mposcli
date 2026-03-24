import logging
import os
from pathlib import Path


logger = logging.getLogger(__name__)


def iter_files(directory):
    with os.scandir(directory) as it:
        for entry in it:
            if entry.is_file(follow_symlinks=False):
                yield entry
            elif entry.is_dir(follow_symlinks=False):
                yield from iter_files(entry.path)


def list_executables(directory: Path) -> list[Path]:
    executables = []
    for entry in directory.iterdir():
        if entry.is_file():
            if os.access(entry, os.X_OK):
                executables.append(entry)
            else:
                logger.warning('%s is not executable! (Hint: "chmod +x <filename>")', entry)
    return executables
