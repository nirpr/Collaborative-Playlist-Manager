from fastapi import FastAPI, HTTPException
from app.auth import get_auth_url, get_access_token
from app.user import User
from fastapi.responses import RedirectResponse
import uuid

app = FastAPI()
user_store = {}


@app.get("/login")
def login():
    auth_url = get_auth_url()
    return RedirectResponse(auth_url)


@app.get("/callback")
def callback(code: str):
    access_token = get_access_token(code)
    user_id = str(uuid.uuid4())
    user = User(user_id, access_token)
    user_store[user_id] = user

    return RedirectResponse(url=f"/user/{user_id}")


@app.get("/user/{user_id}")
def user_data(user_id: str):
    if user_id not in user_store:
        raise HTTPException(status_code=404, detail="User not found")

    user_data = user_store[user_id].get_user_data()

    return {"user_data": user_data}





