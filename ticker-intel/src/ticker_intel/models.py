from pydantic import BaseModel
from datetime import datetime

class ResearchRequest(BaseModel):
    ticker: str
    as_of: datetime
    query: str| None
class SourceDoc(BaseModel):
    url: str
    title: str | None
    retrieved_at: datetime
    content_text: str
class ResearchResult(BaseModel):
    ticker: str
    summary: str 
    bullets: list[str] 
    sources: list[SourceDoc]