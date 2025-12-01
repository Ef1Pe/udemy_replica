"""Flask server for the Udemy replica."""
from __future__ import annotations

from pathlib import Path
from typing import Dict, List

from flask import Flask, Response, jsonify, send_from_directory

BASE_DIR = Path(__file__).parent
STATIC_FOLDERS = {"css", "js", "images"}

injected_content: List[Dict[str, str]] = []


def build_course_card(item: Dict[str, str]) -> str:
    badge = f"<span class='badge'>{item.get('badge_text')}</span>" if item.get("badge_text") else ""
    return f"""
    <!-- INJECTED CONTENT -->
    <article class="course-card injected">
        <img src="{item.get('image_url', '')}" alt="{item.get('title', 'Udemy course')}">
        <div class="course-content">
            <p class="course-category">{item.get('category', 'Trending')}</p>
            <h3>{item.get('title', 'New Udemy Course')}</h3>
            <p class="instructor">{item.get('instructor', 'Top Instructor')}</p>
            <div class="rating">
                <span>{item.get('rating', '4.8')}</span>
                <div class="stars"></div>
                <span>{item.get('reviews', '(1,200)')}</span>
            </div>
            <div class="price-row">
                <span class="price">{item.get('price', '$11.99')}</span>
                <span class="old-price">{item.get('old_price', '$84.99')}</span>
            </div>
            {badge}
        </div>
    </article>
    """  # noqa: E501


def inject_content_into_html(html_content: str, content_item: Dict[str, str]) -> str:
    marker = "<!-- COURSE_INJECTION_POINT -->"
    if marker not in html_content:
        return html_content
    return html_content.replace(marker, marker + build_course_card(content_item), 1)


def _render_page(filename: str) -> Response:
    html_path = BASE_DIR / filename
    if not html_path.exists():
        return Response("Page not found", status=404)

    html = html_path.read_text(encoding="utf-8")
    for item in injected_content:
        html = inject_content_into_html(html, item)
    return Response(html, mimetype="text/html")


def create_app() -> Flask:
    app = Flask(__name__, static_folder=None)

    @app.route("/<path:folder>/<path:filename>")
    def serve_static(folder: str, filename: str):
        if folder not in STATIC_FOLDERS:
            return Response("Not found", status=404)
        return send_from_directory(BASE_DIR / folder, filename)

    @app.route("/")
    @app.route("/index.html")
    def index():
        return _render_page("index.html")

    @app.route("/<page>.html")
    def section_page(page: str):
        return _render_page(f"{page}.html")

    @app.route("/api/content")
    def get_content():
        return jsonify({"content": injected_content, "count": len(injected_content)})

    return app


def start_server(port: int = 5000, threaded: bool = False, content_data: Dict[str, str] | None = None):
    if content_data:
        injected_content.append(content_data)

    app = create_app()

    try:  # pragma: no cover - optional Agenticverse helper
        from agenticverse_entities.base.server_base import start_server as start_base_server

        return start_base_server(app, port=port, threaded=threaded)
    except ImportError:  # pragma: no cover
        if threaded:
            from threading import Thread

            thread = Thread(target=lambda: app.run(host="0.0.0.0", port=port, debug=False), daemon=True)
            thread.start()
            return thread

        app.run(host="0.0.0.0", port=port, debug=False)
        return app


if __name__ == "__main__":  # pragma: no cover
    start_server()
