"""HTTP Range streaming for MP4 files (Safari / mobile video)."""

from __future__ import annotations

import re
from http.server import BaseHTTPRequestHandler
from pathlib import Path


def stream_path(handler: BaseHTTPRequestHandler, path: Path, *, content_type: str = "video/mp4") -> None:
    if not path.is_file():
        handler.send_error(404, "File not found")
        return

    size = path.stat().st_size
    range_header = handler.headers.get("Range")

    if range_header:
        m = re.match(r"bytes=(\d+)-(\d*)", range_header)
        if not m:
            handler.send_error(416, "Invalid Range")
            return
        start = int(m.group(1))
        end = int(m.group(2)) if m.group(2) else size - 1
        end = min(end, size - 1)
        if start > end:
            handler.send_error(416, "Invalid Range")
            return
        length = end - start + 1
        handler.send_response(206)
        handler.send_header("Content-Type", content_type)
        handler.send_header("Accept-Ranges", "bytes")
        handler.send_header("Content-Length", str(length))
        handler.send_header("Content-Range", f"bytes {start}-{end}/{size}")
        handler.end_headers()
        with path.open("rb") as f:
            f.seek(start)
            handler.wfile.write(f.read(length))
        return

    handler.send_response(200)
    handler.send_header("Content-Type", content_type)
    handler.send_header("Accept-Ranges", "bytes")
    handler.send_header("Content-Length", str(size))
    handler.end_headers()
    with path.open("rb") as f:
        while chunk := f.read(1024 * 512):
            handler.wfile.write(chunk)
