import os
import tempfile
import threading
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

import pytest
from testcontainers.postgres import PostgresContainer
from typer.testing import CliRunner

from sightcall_qa_api.indexation.presentation.cli.indexation import app

SITEMAP_XML = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>http://localhost:4987/page1.html</loc>
  </url>
</urlset>
"""

PAGE1_HTML = """
<html><head><title>Test Page</title></head><body>Hello Haystack!</body></html>
"""


@pytest.fixture(scope="module")
def temp_http_server():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        (tmp_path / "sitemap.xml").write_text(SITEMAP_XML, encoding="utf-8")
        (tmp_path / "page1.html").write_text(PAGE1_HTML, encoding="utf-8")
        os.chdir(tmp_path)
        server = HTTPServer(("localhost", 4987), SimpleHTTPRequestHandler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            yield "http://localhost:4987/sitemap.xml"
        finally:
            server.shutdown()
            server.server_close()
            thread.join()


@pytest.fixture(scope="module")
def pgvector_container():
    with PostgresContainer("pgvector/pgvector:pg17", driver=None) as postgres:
        postgres.start()
        yield postgres.get_connection_url()


def test_should_index_content(temp_http_server, pgvector_container):
    runner = CliRunner()
    result = runner.invoke(app, [temp_http_server, "--policy", "overwrite", "--database-url", pgvector_container])
    assert result.exit_code == 0, result.stdout
    assert "Successfully indexed" in result.stdout
    assert "1" in result.stdout or "document" in result.stdout.lower()
