from fastapi import FastAPI, HTTPException
from app.auth import get_auth_url, get_access_token
from app.User import User
from app.User_store import UserStore
from fastapi.responses import RedirectResponse
import uuid

app = FastAPI()
user_store = UserStore()


@app.get("/login")
def login():
    auth_url = get_auth_url()
    return RedirectResponse(auth_url)


@app.get("/callback")
def callback(code: str):
    access_token = get_access_token(code)
    user_id = str(uuid.uuid4())
    user = User(user_id, access_token)
    user_store.add_user(user)

    return RedirectResponse(url=f"/user/{user_id}")


@app.get("/user/{user_id}")
def user_data(user_id: str):
    if user_id not in user_store:
        raise HTTPException(status_code=404, detail="User not found")

    user = user_store.get_user(user_id)

    return {"user_data": user.get_user_data(), "user_top_tracks": user.get_user_top_tracks()}





