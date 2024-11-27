from fastapi import FastAPI
from app.auth import get_auth_url, get_access_token

app = FastAPI()


@app.get("/login")
def login():
    auth_url = get_auth_url()
    return {"auth_url": auth_url}


@app.get("/callback")
def callback(code: str):
    access_token = get_access_token(code)
    return {"access_token": access_token}


#add
