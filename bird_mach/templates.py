"""HTML template helpers for the Mach web application."""

from __future__ import annotations

from bird_mach.constants import APP_NAME, APP_VERSION, DEFAULT_DARK_BG


def base_meta(*, title: str = APP_NAME, description: str = "") -> str:
    """Return common <head> meta tags."""
    return f"""<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="{DEFAULT_DARK_BG}">
<meta name="description" content="{description or f'{APP_NAME} audio visualization'}">
<title>{title}</title>"""


def error_page(*, title: str = "Error", message: str = "Something went wrong") -> str:
    """Render a minimal error page."""
    return f"""<!DOCTYPE html>
<html lang="en"><head>{base_meta(title=f"{title} — {APP_NAME}")}</head>
<body style="background:{DEFAULT_DARK_BG};color:#e2e8f0;font-family:system-ui;padding:2rem;text-align:center">
<h1 style="color:#f87171">{title}</h1>
<p>{message}</p>
<a href="/" style="color:#38bdf8">Back to home</a>
</body></html>"""


def footer_html() -> str:
    """Render the standard footer."""
    return f'<footer style="text-align:center;padding:1rem;color:#64748b;font-size:0.8rem">{APP_NAME} v{APP_VERSION}</footer>'
