from pydantic import BaseModel

from sightcall_qa_api.qa.domain.models.retrieved_document import RetrievedDocument


class Response(BaseModel):
    answer: str
    sources: list[RetrievedDocument]
