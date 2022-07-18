from ..questions.schemas import QuestionResponse
from ..answers.schemas import AnswerResponseWithVotes
from datetime import datetime
from pydantic import BaseModel


class AnswerWithQuestion(BaseModel):
    question: str
    answer: AnswerResponseWithVotes

class UserProfileResponse(BaseModel):
    userId: int
    username: str
    bio: str
    createTime: datetime
    questions: list[QuestionResponse]
    answers: list[AnswerWithQuestion]

class UpdateBio(BaseModel):
    newBio: str
