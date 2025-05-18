import random
import time
import xml.etree.ElementTree as ET
from typing import List

from haystack import component

from sightcall_qa_api.indexation.domain.models.url import Url
from sightcall_qa_api.indexation.domain.ports.http_client import HTTPClient


@component
class SitemapCrawler:
    def __init__(
        self,
        http_client: HTTPClient,
        max_attempts: int = 5,
        base_delay_seconds: float = 12.0,
        max_delay_seconds: float = 120.0,
    ) -> None:
        self._http_client = http_client
        self._max_attempts = max_attempts
        self._base_delay_seconds = base_delay_seconds
        self._max_delay_seconds = max_delay_seconds

    @component.output_types(urls=List[str])
    def run(self, root_url: str) -> dict:
        visited_urls: set[Url] = set()
        collected_links: list[Url] = []
        self._recursively_collect_links(Url(root_url), visited_urls, collected_links)
        return {"urls": [link.value for link in collected_links]}

    def _recursively_collect_links(self, url: Url, visited_urls: set[Url], collected_links: list[Url]) -> None:
        if self._has_already_visited(url, visited_urls):
            return
        self._mark_as_visited(url, visited_urls)
        sitemap_xml = self._get_with_retry(url)
        parsed_urls = self._parse_index(sitemap_xml)
        if self._contains_sitemap_indexes(parsed_urls):
            self._recurse_on_sitemap_indexes(parsed_urls, visited_urls, collected_links)
        else:
            collected_links.extend(parsed_urls)

    def _has_already_visited(self, url: Url, visited_urls: set[Url]) -> bool:
        return url in visited_urls

    def _mark_as_visited(self, url: Url, visited_urls: set[Url]) -> None:
        visited_urls.add(url)

    def _contains_sitemap_indexes(self, urls: list[Url]) -> bool:
        return any(self._is_sitemap_index(url) for url in urls)

    def _is_sitemap_index(self, url: Url) -> bool:
        return url.value.endswith(".xml")

    def _recurse_on_sitemap_indexes(self, urls: list[Url], visited_urls: set[Url], collected_links: list[Url]) -> None:
        for url in urls:
            if self._is_sitemap_index(url):
                self._recursively_collect_links(url, visited_urls, collected_links)

    def _parse_index(self, sitemap_xml: str) -> list[Url]:
        root = ET.fromstring(sitemap_xml)
        namespace = {"ns": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        if root.tag.endswith("urlset"):
            locations = root.findall(".//ns:loc", namespace)
        elif root.tag.endswith("sitemapindex"):
            locations = root.findall(".//ns:loc", namespace)
        else:
            locations = []
        return [Url(location.text) for location in locations if location.text is not None]

    def _get_with_retry(self, url: Url) -> str:
        delay = self._base_delay_seconds
        last_exception: Exception | None = None
        for _ in range(self._max_attempts):
            try:
                return self._http_client.get(url)
            except (ConnectionError, TimeoutError) as error:
                last_exception = error
                time.sleep(delay)
                delay = self._get_next_delay(delay)
            except Exception as error:
                raise RuntimeError(f"[ERR_FETCH_UNEXPECTED] Failed to fetch {url.value}: {error}") from error
        raise RuntimeError(
            f"[ERR_FETCH_MAX_RETRIES] Failed to fetch {url.value} after {self._max_attempts} attempts: {last_exception}"
        )

    def _get_next_delay(self, current_delay: float) -> float:
        return min(current_delay * 2, self._max_delay_seconds) * random.uniform(0.8, 1.2)
