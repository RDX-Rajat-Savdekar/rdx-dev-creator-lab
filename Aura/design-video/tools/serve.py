#!/usr/bin/env python3
"""Local server for the Aura script workspace (side-by-side viewer + save).

Serves tools/index.html and read/write API for markdown in design-video/.

Usage (from repo root or design-video/):
    python Aura/design-video/tools/serve.py
    # → http://127.0.0.1:8765/
"""

from __future__ import annotations

import json
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlparse

from parse_script import export_teleprompter_text, parse_script, summarize_by_chapter

TOOLS_DIR = Path(__file__).resolve().parent
DESIGN_VIDEO = TOOLS_DIR.parent

ALLOWED_MD = frozenset(
    {
        "SCRIPT.md",
        "SCENE-PLAN.md",
        "HACKATHON-STORY.md",
    }
)


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(TOOLS_DIR), **kwargs)

    def do_GET(self) -> None:
        if self.path.startswith("/api/md/"):
            self._handle_get_md()
            return
        if self.path.startswith("/api/script/lines"):
            self._handle_script_lines()
            return
        if self.path.startswith("/api/script/teleprompter.txt"):
            self._handle_teleprompter_export()
            return
        if self.path in ("/", ""):
            self.path = "/index.html"
        super().do_GET()

    def do_PUT(self) -> None:
        if self.path.startswith("/api/md/"):
            self._handle_put_md()
            return
        self.send_error(405, "Method Not Allowed")

    def _handle_get_md(self) -> None:
        name = self._md_name_from_path()
        if name is None:
            return
        path = DESIGN_VIDEO / name
        if not path.is_file():
            self.send_error(404, f"Not found: {name}")
            return
        self._json(200, {"name": name, "content": path.read_text(encoding="utf-8")})

    def _handle_put_md(self) -> None:
        name = self._md_name_from_path()
        if name is None:
            return
        length = int(self.headers.get("Content-Length", 0))
        try:
            payload = json.loads(self.rfile.read(length))
        except json.JSONDecodeError:
            self.send_error(400, "Invalid JSON")
            return
        content = payload.get("content")
        if not isinstance(content, str):
            self.send_error(400, "Missing content string")
            return
        (DESIGN_VIDEO / name).write_text(content, encoding="utf-8")
        self._json(200, {"ok": True, "name": name})

    def _read_script_md(self) -> str:
        return (DESIGN_VIDEO / "SCRIPT.md").read_text(encoding="utf-8")

    def _query_wpm(self) -> float:
        qs = parse_qs(urlparse(self.path).query)
        try:
            return float(qs.get("wpm", ["140"])[0])
        except ValueError:
            return 140.0

    def _query_chapter(self) -> int | None:
        qs = parse_qs(urlparse(self.path).query)
        raw = qs.get("chapter", [None])[0]
        if raw is None or raw == "all":
            return None
        try:
            return int(raw)
        except ValueError:
            return None

    def _handle_script_lines(self) -> None:
        wpm = self._query_wpm()
        lines = parse_script(self._read_script_md(), wpm=wpm)
        self._json(
            200,
            {
                "wpm": wpm,
                "lines": [ln.to_dict() for ln in lines],
                "chapters": summarize_by_chapter(lines),
                "total_words": sum(ln.word_count for ln in lines),
                "total_seconds": round(sum(ln.target_seconds for ln in lines), 1),
            },
        )

    def _handle_teleprompter_export(self) -> None:
        wpm = self._query_wpm()
        chapter = self._query_chapter()
        lines = parse_script(self._read_script_md(), wpm=wpm)
        body = export_teleprompter_text(lines, chapter=chapter).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _md_name_from_path(self) -> str | None:
        name = unquote(self.path.split("/api/md/", 1)[1].split("?", 1)[0])
        if name not in ALLOWED_MD:
            self.send_error(403, f"Not allowed: {name}")
            return None
        return name

    def _json(self, code: int, obj: dict) -> None:
        body = json.dumps(obj).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt: str, *args) -> None:
        print(f"[script-workspace] {args[0]}")


def main() -> None:
    port = 8765
    host = "127.0.0.1"
    server = ThreadingHTTPServer((host, port), Handler)
    print(f"Aura script workspace → http://{host}:{port}/")
    print(f"VO prompter          → http://{host}:{port}/prompter.html")
    print(f"Saves markdown to → {DESIGN_VIDEO}")
    print("Press Ctrl+C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")


if __name__ == "__main__":
    main()
