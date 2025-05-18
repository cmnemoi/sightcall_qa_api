import logging

from haystack import AsyncPipeline
from haystack.components.converters import HTMLToDocument
from haystack.components.embedders import OpenAIDocumentEmbedder
from haystack.components.fetchers import LinkContentFetcher
from haystack.components.preprocessors import RecursiveDocumentSplitter
from haystack.components.writers import DocumentWriter
from haystack.document_stores.types import DocumentStore, DuplicatePolicy

from sightcall_qa_api.config import Config
from sightcall_qa_api.indexation.application.sitemap_crawler import SitemapCrawler
from sightcall_qa_api.indexation.domain.models.url import Url
from sightcall_qa_api.indexation.domain.ports.http_client import HTTPClient

logging.basicConfig(format="%(levelname)s - %(name)s -  %(message)s", level=logging.WARNING)
logging.getLogger("haystack").setLevel(logging.INFO)


class HaystackIndexer:
    def __init__(self, config: Config, http_client: HTTPClient, document_store: DocumentStore):
        self.config = config
        self.http_client = http_client
        self.document_store = document_store

    def run(self, sitemap_url: Url, policy: DuplicatePolicy = DuplicatePolicy.OVERWRITE) -> int:
        indexing = AsyncPipeline()
        indexing.add_component("crawler", SitemapCrawler(self.http_client))  # type: ignore
        indexing.add_component("fetcher", LinkContentFetcher(retry_attempts=5))  # type: ignore
        indexing.add_component("converter", HTMLToDocument())  # type: ignore
        indexing.add_component("splitter", RecursiveDocumentSplitter(split_length=self.config.indexation_split_length))  # type: ignore
        indexing.add_component("embedder", OpenAIDocumentEmbedder(model=self.config.embedding_model))  # type: ignore
        indexing.add_component("writer", DocumentWriter(self.document_store, policy=policy))  # type: ignore
        indexing.connect("crawler", "fetcher")
        indexing.connect("fetcher", "converter")
        indexing.connect("converter", "splitter")
        indexing.connect("splitter", "embedder")
        indexing.connect("embedder", "writer")
        result = indexing.run(data={"crawler": {"root_url": sitemap_url.value}})
        return result["writer"]["documents_written"]
