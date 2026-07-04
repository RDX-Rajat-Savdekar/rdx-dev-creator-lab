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
from parse_vo_docs import export_teleprompter_txt as export_vo_txt
from parse_vo_docs import parse_all_vo_docs, summarize_chapters
from stream_file import stream_path
from video_catalog import build_catalog, resolve_act_path, resolve_chapter_path

TOOLS_DIR = Path(__file__).resolve().parent
DESIGN_VIDEO = TOOLS_DIR.parent
MEDIA = DESIGN_VIDEO / "aura_manim" / "media" / "videos"

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
        if self.path.startswith("/api/vo/teleprompter.json"):
            self._handle_teleprompter_json()
            return
        if self.path.startswith("/api/script/teleprompter.txt"):
            self._handle_teleprompter_export()
            return
        if self.path.startswith("/api/videos/catalog"):
            self._handle_video_catalog()
            return
        if self.path.startswith("/api/videos/act"):
            self._handle_video_act()
            return
        if self.path.startswith("/api/videos/chapter"):
            self._handle_video_chapter()
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

    def _vo_lines(self, wpm: float) -> list[dict]:
        """Prefer vo/sceneN.md (full script); fall back to SCRIPT.md tables."""
        vo_lines = parse_all_vo_docs(wpm=wpm)
        if vo_lines:
            return [
                {
                    "chapter": ln.chapter,
                    "chapter_title": ln.youtube_chapter,
                    "act": ln.act,
                    "line_index": ln.act - 1,
                    "narration": ln.narration,
                    "on_screen": ln.on_screen,
                    "visual": "",
                    "word_count": ln.word_count,
                    "target_seconds": ln.target_seconds,
                }
                for ln in vo_lines
            ]
        legacy = parse_script(self._read_script_md(), wpm=wpm)
        return [ln.to_dict() for ln in legacy]

    def _handle_teleprompter_json(self) -> None:
        """Fallback JSON bundle for prompter (also used when lines API unavailable)."""
        wpm = self._query_wpm()
        cache = DESIGN_VIDEO / "vo" / "teleprompter.json"
        if cache.is_file():
            payload = json.loads(cache.read_text(encoding="utf-8"))
            payload["wpm"] = wpm
            for ln in payload.get("lines", []):
                words = ln.get("word_count", 0)
                ln["target_seconds"] = round((words / wpm) * 60, 1) if words else 0.0
        else:
            vo_lines = parse_all_vo_docs(wpm=wpm)
            if not vo_lines:
                self.send_error(404, "Run build_teleprompter.py first")
                return
            lines = self._vo_lines(wpm)
            payload = {
                "wpm": wpm,
                "lines": lines,
                "chapters": summarize_chapters(vo_lines),
                "total_words": sum(ln["word_count"] for ln in lines),
                "total_seconds": round(sum(ln["target_seconds"] for ln in lines), 1),
                "source": "vo/sceneN.md",
            }
        self._json(200, payload)

    def _handle_script_lines(self) -> None:
        wpm = self._query_wpm()
        vo_lines = parse_all_vo_docs(wpm=wpm)
        lines = self._vo_lines(wpm)
        chapters = (
            summarize_chapters(vo_lines)
            if vo_lines
            else summarize_by_chapter(parse_script(self._read_script_md(), wpm=wpm))
        )
        self._json(
            200,
            {
                "wpm": wpm,
                "lines": lines,
                "chapters": chapters,
                "total_words": sum(ln["word_count"] for ln in lines),
                "total_seconds": round(sum(ln["target_seconds"] for ln in lines), 1),
                "source": "vo/sceneN.md" if vo_lines else "SCRIPT.md",
            },
        )

    def _handle_teleprompter_export(self) -> None:
        wpm = self._query_wpm()
        chapter = self._query_chapter()
        vo_lines = parse_all_vo_docs(wpm=wpm)
        if vo_lines:
            body = export_vo_txt(vo_lines, chapter=chapter).encode("utf-8")
        else:
            lines = parse_script(self._read_script_md(), wpm=wpm)
            body = export_teleprompter_text(lines, chapter=chapter).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _query_str(self, key: str, default: str | None = None) -> str | None:
        qs = parse_qs(urlparse(self.path).query)
        vals = qs.get(key)
        return vals[0] if vals else default

    def _handle_video_catalog(self) -> None:
        self._json(200, build_catalog())

    def _handle_video_act(self) -> None:
        try:
            chapter = int(self._query_str("chapter", "0") or "0")
            act = int(self._query_str("act", "1") or "1")
        except ValueError:
            self.send_error(400, "chapter and act required")
            return
        quality = self._query_str("quality", "480p15") or "480p15"
        path = resolve_act_path(chapter, act, quality)
        if path is None:
            self.send_error(404, f"No video ch{chapter} act{act} ({quality})")
            return
        stream_path(self, path)

    def _handle_video_chapter(self) -> None:
        try:
            chapter = int(self._query_str("chapter", "0") or "0")
        except ValueError:
            self.send_error(400, "chapter required")
            return
        variant = self._query_str("variant", "2160p60") or "2160p60"
        if variant == "480p15":
            preview = (
                MEDIA
                / f"scene{chapter}_full"
                / "480p15"
                / f"Scene{chapter}Full.mp4"
            )
            if preview.is_file():
                stream_path(self, preview)
                return
        path = resolve_chapter_path(chapter, variant)
        if path is None:
            self.send_error(404, f"No chapter {chapter} video ({variant})")
            return
        stream_path(self, path)

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
    import argparse
    import errno
    import socket

    parser = argparse.ArgumentParser(description="Aura script workspace + VO prompter")
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument(
        "--host",
        default="0.0.0.0",
        help="Bind address (0.0.0.0 = phone on same Wi‑Fi can open prompter)",
    )
    args = parser.parse_args()

    try:
        server = ThreadingHTTPServer((args.host, args.port), Handler)
    except OSError as exc:
        if exc.errno == errno.EADDRINUSE:
            print(f"Port {args.port} already in use — an old server is still running.")
            print("Stop it, then start again:")
            print(f"  lsof -ti :{args.port} | xargs kill")
            print(f"  python Aura/design-video/tools/serve.py")
            raise SystemExit(1) from exc
        raise

    lan = "127.0.0.1"
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        lan = s.getsockname()[0]
        s.close()
    except OSError:
        pass

    print(f"Aura script workspace → http://127.0.0.1:{args.port}/")
    print(f"VO prompter (Mac)     → http://127.0.0.1:{args.port}/prompter.html")
    if args.host == "0.0.0.0":
        print(f"VO prompter (phone)   → http://{lan}:{args.port}/prompter.html")
        print("  Same Wi‑Fi as this Mac · use Record mode + video sync")
    print(f"Saves markdown to → {DESIGN_VIDEO}")
    print("Press Ctrl+C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")


if __name__ == "__main__":
    main()
