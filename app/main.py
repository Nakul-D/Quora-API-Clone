from .routers.auth import auth
from fastapi import FastAPI


app = FastAPI()

app.include_router(auth.router)

@app.get('/')
def root():
    return {"message": "Welcome to Quora API Clone"}
