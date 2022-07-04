from .routers.auth import auth
from .routers.questions import questions
from fastapi import FastAPI


app = FastAPI()

app.include_router(auth.router)
app.include_router(questions.router)

@app.get('/')
def root():
    return {"message": "Welcome to Quora API Clone"}
