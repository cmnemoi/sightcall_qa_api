from sightcall_qa_api.indexation.domain.models.url import Url
from sightcall_qa_api.indexation.domain.ports.http_client import HTTPClient


class StubHTTPClient(HTTPClient):
    def __init__(self, url_to_content: dict[Url, str]):
        self._url_to_content = url_to_content

    def get(self, url: Url) -> str:
        if url not in self._url_to_content:
            raise RuntimeError(f"404 Not Found: {url.value}")
        return self._url_to_content[url]
