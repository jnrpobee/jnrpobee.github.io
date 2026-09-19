#!/usr/bin/env python3
"""Local preview server that behaves the way GitHub Pages does.

Python's built-in http.server only serves files at their exact names, so a
link to /research would 404 locally even though it works fine once deployed.
This resolves extensionless paths to their .html files, serves 404.html with a
real 404 status, and is otherwise the standard static file server.

Run it with start-local.bat (Windows) or start-local.sh, or directly:

    python serve.py [port]
"""
import http.server
import functools
import os
import pathlib
import socketserver
import sys
import webbrowser

ROOT = pathlib.Path(__file__).parent.resolve()
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8000


class Handler(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path):
        local = pathlib.Path(super().translate_path(path)).resolve()

        # Never serve anything outside the site folder.
        try:
            local.relative_to(ROOT)
        except ValueError:
            return str(ROOT / "404.html")

        if local.is_dir():
            index = local / "index.html"
            if index.is_file():
                return str(index)

        # /research -> research.html, the way GitHub Pages resolves it.
        if not local.exists() and not local.suffix:
            candidate = local.with_suffix(".html")
            if candidate.is_file():
                return str(candidate)

        return str(local)

    def send_head(self):
        # A path that resolved to nothing gets the site's own 404 page, with a
        # 404 status rather than a 200, so the local preview does not quietly
        # differ from production.
        local = pathlib.Path(self.translate_path(self.path))
        if not local.exists():
            body = (ROOT / "404.html").read_bytes()
            self.send_response(404)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            return __import__("io").BytesIO(body)
        return super().send_head()

    def log_message(self, fmt, *args):
        sys.stderr.write("  %s\n" % (fmt % args))


def main():
    os.chdir(ROOT)
    socketserver.TCPServer.allow_reuse_address = True
    handler = functools.partial(Handler, directory=str(ROOT))
    try:
        with socketserver.TCPServer(("127.0.0.1", PORT), handler) as httpd:
            url = "http://localhost:%d/" % PORT
            print("\n  Site running at %s" % url)
            print("  Clean URLs work here exactly as they do live.")
            print("  Press Ctrl+C to stop.\n")
            try:
                webbrowser.open(url)
            except Exception:
                pass
            httpd.serve_forever()
    except OSError as e:
        print("\n  Could not start on port %d: %s" % (PORT, e))
        print("  Something else may be using it. Try: python serve.py 8001\n")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n  Stopped.\n")


if __name__ == "__main__":
    main()
