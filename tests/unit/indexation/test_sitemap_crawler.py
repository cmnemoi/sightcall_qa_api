from sightcall_qa_api.indexation.application.sitemap_crawler import SitemapCrawler
from sightcall_qa_api.indexation.domain.models.url import Url
from sightcall_qa_api.indexation.infrastructure.for_tests.stub_http_client import StubHTTPClient


def test_sitemap_crawler_should_collect_all_links_from_nested_sitemaps():
    root_index_url, http_client = given_some_sitemaps()
    all_links = when_crawling_all_links(root_index_url, http_client)
    then_all_links_are_collected(all_links)


def given_some_sitemaps() -> tuple[Url, StubHTTPClient]:
    root_index_url = Url("https://sightcall.com/sitemap_index.xml")
    post_sitemap_url = Url("https://sightcall.com/post-sitemap.xml")
    page_sitemap_url = Url("https://sightcall.com/page-sitemap.xml")
    sitemap_index_xml = """<?xml version="1.0" encoding="UTF-8"?>
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <sitemap><loc>https://sightcall.com/post-sitemap.xml</loc></sitemap>
    <sitemap><loc>https://sightcall.com/page-sitemap.xml</loc></sitemap>
</sitemapindex>"""
    post_sitemap_xml = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url><loc>https://sightcall.com/post/1</loc></url>
    <url><loc>https://sightcall.com/post/2</loc></url>
</urlset>"""
    page_sitemap_xml = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url><loc>https://sightcall.com/page/1</loc></url>
</urlset>"""
    http_client = StubHTTPClient(
        {
            root_index_url: sitemap_index_xml,
            post_sitemap_url: post_sitemap_xml,
            page_sitemap_url: page_sitemap_xml,
        }
    )
    return root_index_url, http_client


def when_crawling_all_links(root_index_url: Url, http_client: StubHTTPClient) -> list[str]:
    crawler = SitemapCrawler(http_client=http_client)
    result = crawler.run(root_index_url.value)
    return result["urls"]


def then_all_links_are_collected(all_links: list[str]):
    expected_links = [
        "https://sightcall.com/post/1",
        "https://sightcall.com/post/2",
        "https://sightcall.com/page/1",
    ]
    assert sorted(all_links) == sorted(expected_links)
