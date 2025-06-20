from pydantic import BaseModel

class DocumentUploadRequest(BaseModel):
    semester: str
    subject: str

class ChatRequest(BaseModel):
    query: str
