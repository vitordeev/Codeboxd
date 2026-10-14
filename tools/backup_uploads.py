"""Create and verify a private ZIP snapshot of local uploads without deleting them."""
import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


ROOT = Path(__file__).resolve().parents[1]


def backup(source: Path, destination: Path) -> dict:
    source = source.resolve(strict=True)
    destination = destination.resolve()
    if not source.is_dir():
        raise ValueError('Upload source must be a directory')
    if destination == source or source in destination.parents:
        raise ValueError('Backup must be outside the upload source')
    # Refuse links before reading so a snapshot cannot traverse outside uploads.
    entries = sorted(source.rglob('*'))
    if any(path.is_symlink() or path.is_junction() for path in entries):
        raise ValueError('Upload source contains a link; review it before backup')
    files = [path for path in entries if path.is_file()]
    if not files:
        raise ValueError('No upload files found; no empty backup was created')
    destination.parent.mkdir(parents=True, exist_ok=True)
    manifest = {}
    total_bytes = 0
    # Exclusive creation preserves earlier backups, including on a repeated run.
    with ZipFile(destination, 'x', compression=ZIP_DEFLATED) as archive:
        for path in files:
            name = path.relative_to(source).as_posix()
            content = path.read_bytes()
            manifest[name] = hashlib.sha256(content).hexdigest()
            total_bytes += len(content)
            archive.writestr('uploaded_files/' + name, content)
        archive.writestr('manifest.json', json.dumps(manifest, indent=2))
    with ZipFile(destination) as archive:
        if archive.testzip() is not None:
            raise ValueError('Backup archive failed CRC verification')
        for name, digest in manifest.items():
            if hashlib.sha256(archive.read('uploaded_files/' + name)).hexdigest() != digest:
                raise ValueError('Backup content failed SHA-256 verification')
    return {'files': len(files), 'source_bytes': total_bytes, 'verified': True,
            'archive_sha256': hashlib.sha256(destination.read_bytes()).hexdigest()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, default=ROOT / 'uploaded_files')
    parser.add_argument('--destination', type=Path)
    args = parser.parse_args()
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    destination = args.destination or ROOT / '.local' / 'backups' / f'uploads-{stamp}.zip'
    result = backup(args.source, destination)
    print(json.dumps({'backup': str(destination), **result}, indent=2))


if __name__ == '__main__':
    main()
