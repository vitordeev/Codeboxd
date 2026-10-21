"""Prepare independent Reflex generated files without touching a running frontend."""
from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parents[1]


def prepare_frontend(name: str) -> Path:
    """Copy sources and packages once; never mutate a running frontend's files.

    Build output, Vite caches, packages and backend artifacts belong to each
    workdir, including when Reflex decides dependencies need installation.
    """
    if not name or any(c not in 'abcdefghijklmnopqrstuvwxyz0123456789-' for c in name):
        raise ValueError('Use a lowercase frontend name containing letters, digits or hyphens')
    destination = ROOT / '.local' / 'frontends' / name
    if destination.exists():
        raise FileExistsError(f'Preserve existing frontend: {destination}')
    source = ROOT / '.web'
    def ignore(directory, names):
        # Packages can contain required directories named "build" or "backend".
        excluded = {'.vite'}
        if Path(directory) == source:
            excluded.update({'build', '.react-router', 'backend',
                             '.reflex_dev_backend_started'})
        return excluded.intersection(names)
    shutil.copytree(source, destination, ignore=ignore)
    return destination
