from datetime import datetime
from pydantic import BaseModel


class PostAnswer(BaseModel):
    answer: str


class AnswerResponse(BaseModel):
    answerId: int
    questionId: int
    answer: str
    userId: int
    createTime: datetime
    lastUpdated: datetime
    edited: bool

    class Config:
        orm_mode = True

class AnswerResponseWithVotes(AnswerResponse):
    upVotes: int
    downVotes: int
    currentUserUpVoted: bool | None
