import pytest

from sightcall_qa_api.indexation.application.sitemap_crawler import SitemapCrawler
from sightcall_qa_api.indexation.domain.models.url import Url
from sightcall_qa_api.indexation.infrastructure.for_production.httpx_client import HTTPXClient


class TestSitemapCrawlerIntegration:
    def test_should_collect_links_from_category_sitemap(self):
        http_client = self._given_real_http_client()
        root_url = self._given_category_sitemap_url()
        all_links = self._when_crawling_all_links(root_url, http_client)
        self._then_should_collect_at_least_one_link(all_links)

    def test_should_fail_on_invalid_url(self):
        http_client = self._given_real_http_client()
        invalid_url = Url("https://sightcall.com/this-sitemap-does-not-exist.xml")
        with pytest.raises(RuntimeError) as exc_info:
            self._when_crawling_all_links(invalid_url, http_client)
        assert "Failed to fetch" in str(exc_info.value) or "404" in str(exc_info.value)

    def _given_real_http_client(self):
        return HTTPXClient()

    def _given_category_sitemap_url(self):
        return Url("https://sightcall.com/category-sitemap.xml")

    def _when_crawling_all_links(self, root_url: Url, http_client: HTTPXClient):
        crawler = SitemapCrawler(http_client=http_client)
        result = crawler.run(root_url.value)
        return result["urls"]

    def _then_should_collect_at_least_one_link(self, all_links):
        assert isinstance(all_links, list)
        assert all_links, "No links collected from category sitemap."
        for link in all_links:
            assert isinstance(link, str)
            assert link.startswith("https://sightcall.com/"), f"Unexpected link: {link}"
