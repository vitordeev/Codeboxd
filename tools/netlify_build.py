"""Build the Reflex static frontend for Netlify."""

from __future__ import annotations

import os
import re
import subprocess
import sys
from urllib.parse import urlsplit


def validate_api_url(raw_url: str) -> str:
    url = raw_url.strip()
    parsed = urlsplit(url)
    host = (parsed.hostname or "").lower()
    if (
        parsed.scheme != "https"
        or not host
        or "." not in host
        or host in {"localhost", "127.0.0.1", "0.0.0.0", "::1"}
        or host.endswith(".localhost")
        or host.endswith(".invalid")
        or host.endswith(".example")
        or host.endswith(".test")
        or parsed.username is not None
        or parsed.password is not None
        or parsed.query
        or parsed.fragment
        or not re.fullmatch(r"[A-Za-z0-9.-]+", host)
    ):
        raise ValueError(
            "REFLEX_API_URL deve ser uma URL HTTPS pública do backend Reflex, "
            "sem credenciais, query ou fragmento. Configure-a nas variáveis "
            "de ambiente da Netlify."
        )
    return url.rstrip("/")


def main() -> int:
    try:
        os.environ["REFLEX_API_URL"] = validate_api_url(
            os.environ.get("REFLEX_API_URL", "")
        )
    except ValueError as exc:
        print(f"Erro de configuração Netlify: {exc}", file=sys.stderr)
        return 2

    command = [
        sys.executable,
        "-m",
        "reflex",
        "export",
        "--frontend-only",
        "--no-zip",
        "--env",
        "prod",
    ]
    subprocess.run(command, check=True)

    output = os.path.join(".web", "build", "client", "index.html")
    if not os.path.isfile(output):
        print(
            f"A exportação Reflex terminou sem gerar {output}.", file=sys.stderr
        )
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
