from abc import ABC, abstractmethod

from sightcall_qa_api.indexation.domain.models.url import Url


class HTTPClient(ABC):
    @abstractmethod
    def get(self, url: Url) -> str:
        pass
