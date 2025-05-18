from fastapi import Depends
from haystack.components.embedders import OpenAITextEmbedder
from haystack.components.generators import OpenAIGenerator
from haystack.document_stores.types import DocumentStore
from haystack.utils import Secret
from haystack_integrations.components.retrievers.pgvector import PgvectorEmbeddingRetriever
from haystack_integrations.document_stores.pgvector import PgvectorDocumentStore

from sightcall_qa_api.config import Config

config = Config()


def get_document_store() -> DocumentStore:
    return PgvectorDocumentStore(
        connection_string=Secret.from_env_var("DATABASE_URL"), embedding_dimension=config.embedding_dimension
    )


def get_embedder() -> OpenAITextEmbedder:
    return OpenAITextEmbedder(model=config.embedding_model)


def get_llm() -> OpenAIGenerator:
    return OpenAIGenerator(model=config.chatbot_model)


def get_retriever(document_store: PgvectorDocumentStore = Depends(get_document_store)) -> PgvectorEmbeddingRetriever:
    return PgvectorEmbeddingRetriever(document_store=document_store)
