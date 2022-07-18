from .routers.auth import auth
from .routers.questions import questions
from .routers.answers import answers
from .routers.votes import votes
from .routers.user import user
from fastapi import FastAPI


app = FastAPI()

app.include_router(auth.router)
app.include_router(questions.router)
app.include_router(answers.router)
app.include_router(votes.router)
app.include_router(user.router)

@app.get('/')
def root():
    return {"message": "Welcome to Quora API Clone"}
