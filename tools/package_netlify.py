"""Create a safe source ZIP for configuring the Codeboxd Netlify deploy."""

from __future__ import annotations

import os
from pathlib import Path
import zipfile


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "dist" / "Codeboxd-Netlify-Source.zip"
ROOT_FILES = (
    ".env.example",
    ".gitignore",
    "README.md",
    "netlify.toml",
    "requirements.txt",
    "rxconfig.py",
)
SOURCE_DIRS = ("Codeboxd_main", "assets", "reflex.lock")
EXTRA_FILES = ("docs/DEPLOY_NETLIFY.md", "tools/netlify_build.py")
EXCLUDED_DIRS = {
    ".git",
    ".local",
    ".venv",
    ".web",
    ".states",
    "__pycache__",
    "external",
    "node_modules",
    "uploaded_files",
    "venv",
    "xano",
}
FORBIDDEN_NAMES = {".env", ".netlify", ".states", ".web", ".local", ".git"}


def safe_file(path: Path) -> bool:
    if not path.is_file() or path.is_symlink():
        return False
    relative = path.relative_to(ROOT)
    parts = relative.parts
    if any(part in EXCLUDED_DIRS for part in parts):
        return False
    if path.name == ".env" or (
        path.name.startswith(".env.") and path.name != ".env.example"
    ):
        return False
    if path.suffix in {".log", ".pyc", ".pyo"}:
        return False
    return True


def selected_files() -> list[Path]:
    candidates: set[Path] = set()
    for relative in ROOT_FILES + EXTRA_FILES:
        candidate = ROOT / relative
        if candidate.exists():
            candidates.add(candidate)
    for directory in SOURCE_DIRS:
        base = ROOT / directory
        if base.exists():
            candidates.update(base.rglob("*"))
    return sorted((p for p in candidates if safe_file(p)), key=lambda p: p.as_posix())


def check_archive(archive: zipfile.ZipFile) -> None:
    names = archive.namelist()
    for name in names:
        parts = Path(name).parts
        if any(part in FORBIDDEN_NAMES for part in parts):
            raise RuntimeError(f"Conteúdo local proibido encontrado no ZIP: {name}")
        basename = Path(name).name
        if basename == ".env" or (
            basename.startswith(".env.") and basename != ".env.example"
        ):
            raise RuntimeError(f"Arquivo de ambiente proibido no ZIP: {name}")
    required = {"netlify.toml", "requirements.txt", "rxconfig.py", ".env.example"}
    missing = required.difference(names)
    if missing:
        raise RuntimeError(f"Arquivos esperados ausentes no ZIP: {sorted(missing)}")


def main() -> int:
    files = selected_files()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(OUTPUT, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in files:
            archive.write(path, path.relative_to(ROOT).as_posix())
        readme = (
            "Pacote-fonte Codeboxd para configurar o deploy na Netlify.\n\n"
            "Este ZIP nao e um site estatico pronto para upload manual: conecte-o "
            "a um repositorio/Netlify CLI, configure REFLEX_API_URL com o backend "
            "publico e execute o build descrito em docs/DEPLOY_NETLIFY.md.\n"
            "O backend Reflex precisa ser hospedado separadamente.\n"
        )
        archive.writestr("PACOTE-NETLIFY.txt", readme)
    with zipfile.ZipFile(OUTPUT) as archive:
        check_archive(archive)
    print(f"Pacote criado: {OUTPUT}")
    print(f"Arquivos incluídos: {len(files) + 1}")
    print(f"Tamanho: {OUTPUT.stat().st_size} bytes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
