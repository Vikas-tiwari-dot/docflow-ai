from pydantic import BaseModel
from datetime import datetime
class DocumentResponse(BaseModel):
    id: int; filename: str; file_type: str; file_size: int; status: str; created_at: datetime; updated_at: datetime
    class Config: from_attributes = True
class DocumentDetail(DocumentResponse):
    extracted_text: str
class AskRequest(BaseModel):
    question: str
class AskResponse(BaseModel):
    answer: str; document_id: int; question: str
class ChatResponse(BaseModel):
    id: int; question: str; answer: str; created_at: datetime
    class Config: from_attributes = True
