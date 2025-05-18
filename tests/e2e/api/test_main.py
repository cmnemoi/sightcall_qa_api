from http import HTTPStatus
from typing import Any
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient
from haystack import Document
from haystack.components.retrievers.in_memory import InMemoryEmbeddingRetriever
from haystack.document_stores.in_memory import InMemoryDocumentStore

from sightcall_qa_api.config import Config
from sightcall_qa_api.qa.presentation.api.dependencies import get_document_store, get_retriever
from sightcall_qa_api.qa.presentation.api.main import app

doc_store: InMemoryDocumentStore = InMemoryDocumentStore()
app.dependency_overrides[get_document_store] = lambda: doc_store
app.dependency_overrides[get_retriever] = lambda: InMemoryEmbeddingRetriever(document_store=doc_store)


@pytest.fixture(scope="module")
def test_client() -> TestClient:
    return TestClient(app)


def should_return_answer_when_given_valid_question(test_client: TestClient) -> None:
    """Should return answer and sources when given a valid question."""
    _given_document_in_store(
        content="SightCall is a video cloud platform.",
        url="https://example.com/doc1",
        embedding=[0.1] * Config().embedding_dimension,
    )
    payload = _given_valid_question_payload()
    response = _when_posting_chat(test_client, payload)
    _then_response_status_is(response, HTTPStatus.OK)
    _then_response_contains_answer_and_sources(response)


def should_return_400_when_question_is_empty(test_client: TestClient) -> None:
    """Should return 400 when the question is empty."""
    payload = _given_empty_question_payload()
    response = _when_posting_chat(test_client, payload)
    _then_response_status_is(response, HTTPStatus.BAD_REQUEST)
    _then_response_error_message_is(response, "Query must not be empty.")


def should_return_500_when_chatbot_raises_exception(test_client: TestClient) -> None:
    """Should return 500 when the chatbot raises an exception."""
    payload = _given_valid_question_payload()
    with patch(
        "sightcall_qa_api.qa.application.haystack_chatbot.HaystackChatbot.answer",
        side_effect=RuntimeError("Simulated failure"),
    ):
        response = _when_posting_chat(test_client, payload)
        _then_response_status_is(response, HTTPStatus.INTERNAL_SERVER_ERROR)
        _then_response_error_message_startswith(response, "Chatbot error:")


def _given_document_in_store(content: str, url: str, embedding: list[float]) -> None:
    doc_store.write_documents([Document(content=content, meta={"url": url}, embedding=embedding)])


def _given_valid_question_payload() -> dict[str, str]:
    return {"question": "What is SightCall?"}


def _given_empty_question_payload() -> dict[str, str]:
    return {"question": ""}


def _when_posting_chat(client: TestClient, payload: dict[str, Any]):
    return client.post("/chat", json=payload)


def _then_response_status_is(response, expected_status: int) -> None:
    assert response.status_code == expected_status


def _then_response_contains_answer_and_sources(response) -> None:
    json_data = response.json()
    assert "answer" in json_data
    assert isinstance(json_data["answer"], str)
    assert json_data["answer"]
    assert "sources" in json_data
    assert isinstance(json_data["sources"], list)
    for source in json_data["sources"]:
        assert "content" in source
        assert "url" in source


def _then_response_error_message_is(response, expected_detail: str) -> None:
    assert response.json()["detail"] == expected_detail


def _then_response_error_message_startswith(response, expected_prefix: str) -> None:
    assert response.json()["detail"].startswith(expected_prefix)
