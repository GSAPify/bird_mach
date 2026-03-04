"""Tests for bird_mach.templates."""

from bird_mach.templates import base_meta, error_page, footer_html


class TestBaseMeta:
    def test_contains_charset(self):
        html = base_meta()
        assert 'charset="utf-8"' in html

    def test_custom_title(self):
        html = base_meta(title="Test Page")
        assert "<title>Test Page</title>" in html


class TestErrorPage:
    def test_contains_message(self):
        html = error_page(message="File not found")
        assert "File not found" in html

    def test_has_back_link(self):
        html = error_page()
        assert 'href="/"' in html


class TestFooter:
    def test_contains_version(self):
        html = footer_html()
        assert "Mach" in html
