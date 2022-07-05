from datetime import datetime
from pydantic import BaseModel

class PostQuestion(BaseModel):
    question: str

class QuestionResponse(BaseModel):
    questionId: int
    userId: int
    question: str
    createTime: datetime
    lastUpdated: datetime
    edited: bool

    class Config:
        orm_mode = True
