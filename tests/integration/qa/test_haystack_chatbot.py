import pytest
from haystack.utils import Secret
from haystack_integrations.components.retrievers.pgvector import PgvectorEmbeddingRetriever
from haystack_integrations.document_stores.pgvector import PgvectorDocumentStore
from testcontainers.postgres import PostgresContainer

from sightcall_qa_api.qa.application.haystack_chatbot import HaystackChatbot
from sightcall_qa_api.qa.infrastructure.for_tests.haystack_deterministic_text_embedder import (
    HaystackDeterministicTextEmbedder,
)
from sightcall_qa_api.qa.infrastructure.for_tests.haystack_determinstic_generator import (
    HaystackDeterminsticTextGenerator,
)


@pytest.fixture(scope="module")
def pgvector_document_store_url():
    with PostgresContainer("pgvector/pgvector:pg17", driver=None) as postgres:
        postgres.start()
        yield postgres.get_connection_url()


def test_haystack_chatbot_returns_answer(pgvector_document_store_url):
    document_store = PgvectorDocumentStore(connection_string=Secret.from_token(pgvector_document_store_url))
    retriever = PgvectorEmbeddingRetriever(document_store=document_store)

    chatbot = HaystackChatbot(
        document_store=document_store,
        embedder=HaystackDeterministicTextEmbedder(embeddings_size=document_store.embedding_dimension),
        llm=HaystackDeterminsticTextGenerator(answer="42"),
        retriever=retriever,
    )
    response = chatbot.answer("What is the meaning of life?")
    assert response.answer == "42"
