from pydantic import BaseModel


class Query(BaseModel):
    question: str = "What is SightCall ?"
