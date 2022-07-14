from .routers.auth import auth
from .routers.questions import questions
from .routers.answers import answers
from .routers.votes import votes
from fastapi import FastAPI


app = FastAPI()

app.include_router(auth.router)
app.include_router(questions.router)
app.include_router(answers.router)
app.include_router(votes.router)

@app.get('/')
def root():
    return {"message": "Welcome to Quora API Clone"}
