from pydantic import BaseModel


class Config(BaseModel):
    chatbot_model: str = "gpt-4o-mini"
    embedding_dimension: int = 3_072
    embedding_model: str = "text-embedding-3-large"
    indexation_split_length: int = 5_000
