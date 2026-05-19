from __future__ import annotations

import os
import urllib.error
import urllib.request
from pathlib import Path
from urllib.parse import urljoin, urlparse

TEXT_EXTENSIONS = {
    "",
    ".html",
    ".htm",
    ".json",
    ".md",
    ".mdx",
    ".txt",
    ".xml",
    ".yaml",
    ".yml",
}

SKIP_DIRS = {
    ".git",
    ".github",
    ".venv",
    "__pycache__",
    "build",
    "dist",
    "examples",
    "node_modules",
    "src",
    "test",
    "tests",
    "fixtures",
}

URL_PATHS = (
    "/",
    "/llms.txt",
    "/robots.txt",
    "/sitemap.xml",
    "/agentic-ready.json",
    "/.well-known/agentic-ready.json",
    "/.well-known/mcp.json",
    "/openapi.json",
    "/openapi.yaml",
    "/swagger.json",
    "/docs",
    "/api",
    "/pricing",
    "/security",
    "/status",
)

USER_AGENT = "agentic-ready/0.1 (+https://github.com/marvinvista/agentic-ready)"


def load_target(target: str, *, timeout: float = 8.0) -> tuple[dict[str, str], tuple[str, ...]]:
    parsed = urlparse(target)
    if parsed.scheme in {"http", "https"}:
        return load_url(target, timeout=timeout)
    return load_path(Path(target))


def load_path(target: Path) -> tuple[dict[str, str], tuple[str, ...]]:
    root = target.resolve()
    if not root.exists():
        raise FileNotFoundError(f"Target does not exist: {target}")

    if root.is_file():
        return {root.name: root.read_text(encoding="utf-8", errors="replace")}, ()

    docs: dict[str, str] = {}
    warnings: list[str] = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [name for name in dirnames if name not in SKIP_DIRS]
        for filename in filenames:
            path = Path(dirpath) / filename
            if path.suffix.lower() not in TEXT_EXTENSIONS:
                continue
            try:
                docs[path.relative_to(root).as_posix()] = path.read_text(encoding="utf-8", errors="replace")
            except OSError as exc:
                warnings.append(f"Could not read {path}: {exc}")
    return docs, tuple(warnings)


def load_url(url: str, *, timeout: float) -> tuple[dict[str, str], tuple[str, ...]]:
    base = url if url.endswith("/") else f"{url}/"
    docs: dict[str, str] = {}
    warnings: list[str] = []
    for path in URL_PATHS:
        candidate = urljoin(base, path)
        try:
            request = urllib.request.Request(candidate, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(request, timeout=timeout) as response:
                content_type = response.headers.get("content-type", "")
                if content_type and not _is_text(content_type):
                    continue
                docs[path.lstrip("/") or "index.html"] = response.read(2_000_000).decode("utf-8", errors="replace")
        except (urllib.error.URLError, TimeoutError, ValueError) as exc:
            warnings.append(f"Could not fetch {candidate}: {exc}")
    return docs, tuple(warnings)


def _is_text(content_type: str) -> bool:
    lowered = content_type.lower()
    return any(token in lowered for token in ("text/", "json", "xml", "yaml", "markdown", "javascript"))
