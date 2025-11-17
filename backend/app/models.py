# backend/app/models.py
from pydantic import BaseModel
from typing import List, Optional

class SearchRequest(BaseModel):
    query: str
    k: int = 5

class IngestItem(BaseModel):
    id: str
    title: str
    body: Optional[str] = ""
    tags: Optional[List[str]] = []

class Feedback(BaseModel):
    question_id: str
    useful: bool
