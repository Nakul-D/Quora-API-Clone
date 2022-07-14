from datetime import datetime
from pydantic import BaseModel


class PostVote(BaseModel):
    upvoted: bool
