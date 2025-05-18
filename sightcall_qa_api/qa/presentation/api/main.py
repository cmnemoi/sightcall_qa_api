import logging
from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from haystack.document_stores.types import DocumentStore

from sightcall_qa_api import __version__
from sightcall_qa_api.qa.application.haystack_chatbot import HaystackChatbot
from sightcall_qa_api.qa.domain.models.query import Query
from sightcall_qa_api.qa.domain.models.response import Response
from sightcall_qa_api.qa.presentation.api.dependencies import get_document_store, get_embedder, get_llm, get_retriever

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("sightcall_qa_api")

app = FastAPI(
    title="SightCall Q&A API", description="A RAG-based API to ask questions about SightCall.", version=__version__
)


@app.post("/chat", response_model=Response)
def chat_endpoint(
    request: Query,
    document_store: DocumentStore = Depends(get_document_store),
    embedder=Depends(get_embedder),
    llm=Depends(get_llm),
    retriever=Depends(get_retriever),
):
    if not request.question:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Query must not be empty.")
    try:
        chatbot = HaystackChatbot(document_store, embedder, llm, retriever)
        return chatbot.answer(request.question)
    except Exception as error:
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail=f"Chatbot error: {error}")
