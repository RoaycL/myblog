# MyBlog

A lightweight personal blog built with Flask. Posts are defined in `content/posts.json` using Markdown and rendered with clean templates.

## Getting started

1. Install dependencies (preferably in a virtual environment):
   ```bash
   pip install -r requirements.txt
   ```
2. Run the development server:
   ```bash
   flask --app app.py --debug run
   ```
3. Open `http://127.0.0.1:5000` to view the blog.

## Adding posts

1. Open `content/posts.json` and append a new object with the following keys:
   - `slug`: URL-safe identifier (e.g., `my-new-post`).
   - `title`: Post title.
   - `date`: ISO date string (`YYYY-MM-DD`).
   - `excerpt`: Short preview text.
   - `tags`: Array of tags.
   - `content`: Markdown content.
2. Restart the Flask app to reload the updated posts list.

## Project structure

- `app.py`: Flask application with routes and post loader.
- `content/posts.json`: Sample posts stored in Markdown-friendly JSON.
- `templates/`: Jinja templates for pages.
- `static/style.css`: Styling for the blog.

## Tests

Compile the project to verify there are no syntax errors:
```bash
python -m compileall .
```
