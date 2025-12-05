from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List

from flask import Flask, abort, render_template, request, url_for
from markdown import markdown


@dataclass
class Post:
    slug: str
    title: str
    date: datetime
    excerpt: str
    tags: List[str]
    content: str

    @property
    def formatted_date(self) -> str:
        return self.date.strftime("%B %d, %Y")


def load_posts(posts_path: Path) -> list[Post]:
    if not posts_path.exists():
        raise FileNotFoundError(f"Unable to locate posts file at {posts_path}")

    with posts_path.open("r", encoding="utf-8") as handle:
        raw_posts = json.load(handle)

    posts: list[Post] = []
    for post in raw_posts:
        html_content = markdown(post["content"], extensions=["fenced_code", "tables"])
        posts.append(
            Post(
                slug=post["slug"],
                title=post["title"],
                date=datetime.fromisoformat(post["date"]),
                excerpt=post["excerpt"],
                tags=post.get("tags", []),
                content=html_content,
            )
        )

    posts.sort(key=lambda post: post.date, reverse=True)
    return posts


def create_app() -> Flask:
    app = Flask(__name__)
    posts = load_posts(Path(__file__).parent / "content" / "posts.json")
    posts_by_slug = {post.slug: post for post in posts}

    @app.context_processor
    def inject_navigation():
        tags = sorted({tag for post in posts for tag in post.tags})
        return {
            "nav_links": [
                {"label": "Home", "href": url_for("index")},
                {"label": "About", "href": url_for("about")},
            ],
            "all_tags": tags,
        }

    @app.route("/")
    def index():
        query = request.args.get("q", "").strip().lower()
        filtered_posts = posts
        if query:
            filtered_posts = [
                post
                for post in posts
                if query in post.title.lower() or query in " ".join(post.tags).lower()
            ]
        return render_template("index.html", posts=filtered_posts, query=query)

    @app.route("/tags/<tag>")
    def tag(tag: str):
        tag_lower = tag.lower()
        tagged_posts = [post for post in posts if tag_lower in (t.lower() for t in post.tags)]
        if not tagged_posts:
            abort(404)
        return render_template("tag.html", posts=tagged_posts, tag=tag)

    @app.route("/posts/<slug>")
    def post(slug: str):
        post_obj = posts_by_slug.get(slug)
        if not post_obj:
            abort(404)
        return render_template("post.html", post=post_obj)

    @app.route("/about")
    def about():
        return render_template("about.html")

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
