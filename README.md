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

## Deployment on a server

Below is a simple process to get the project running on a Linux server (Ubuntu/Debian style). Adjust the username, paths, and domains as needed.

1. **Pull the code**
   ```bash
   # from your home directory or another working path
   git clone https://github.com/your-username/myblog.git
   cd myblog
   ```

2. **Set up Python and dependencies**
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

3. **Run under Gunicorn (example)**
   ```bash
   # still in the project directory with the virtualenv activated
   gunicorn --bind 0.0.0.0:8000 app:app
   ```
   Gunicorn will serve the Flask app on port 8000. Point your reverse proxy (e.g., Nginx, Caddy) at `http://127.0.0.1:8000`.

4. **Create a basic systemd service (optional but recommended)**
   ```bash
   sudo tee /etc/systemd/system/myblog.service > /dev/null <<'EOF'
   [Unit]
   Description=MyBlog Flask app
   After=network.target

   [Service]
   User=www-data
   WorkingDirectory=/home/www-data/myblog
   Environment="PATH=/home/www-data/myblog/.venv/bin"
   ExecStart=/home/www-data/myblog/.venv/bin/gunicorn --bind 0.0.0.0:8000 app:app
   Restart=on-failure

   [Install]
   WantedBy=multi-user.target
   EOF

   sudo systemctl daemon-reload
   sudo systemctl enable --now myblog.service
   ```

5. **Troubleshooting**
   - Check logs: `journalctl -u myblog.service -f`.
   - Verify Gunicorn is listening: `ss -tlnp | grep 8000`.
   - Restart after code updates: `sudo systemctl restart myblog.service`.

If you prefer to keep it simple, you can also start the app with `flask --app app.py run --host 0.0.0.0 --port 8000` and use a process manager like `tmux` or `supervisor` to keep it alive.

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
