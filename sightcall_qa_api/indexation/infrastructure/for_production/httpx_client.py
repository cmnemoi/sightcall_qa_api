import httpx

from sightcall_qa_api.indexation.domain.models.url import Url
from sightcall_qa_api.indexation.domain.ports.http_client import HTTPClient

DEFAULT_USER_AGENT = "Mozilla/5.0 (compatible; IntegrationTestBot/1.0; +https://sightcall.com/)"


class HTTPXClient(HTTPClient):
    """
    HTTPX async adapter for HTTPClient.
    """

    def __init__(self, timeout_seconds: float = 3.0, user_agent: str = DEFAULT_USER_AGENT) -> None:
        self._timeout_seconds = timeout_seconds
        self._user_agent = user_agent

    def get(self, url: Url) -> str:
        headers = {"User-Agent": self._user_agent}
        with httpx.Client(timeout=self._timeout_seconds, headers=headers) as client:
            try:
                response = client.get(url.value)
                response.raise_for_status()
                return response.text
            except httpx.HTTPError as error:
                raise RuntimeError(f"Failed to fetch {url.value}: {error}") from error
