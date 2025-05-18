from pydantic import BaseModel


class RetrievedDocument(BaseModel):
    content: str
    url: str
