from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.auth import get_auth_url, get_access_token
from app.User import User
from app.User_store import UserStore
from app.PlayList import PlayList
from fastapi.responses import RedirectResponse

app = FastAPI()
app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8001"],  # Frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
FRONTEND_URL = "http://127.0.0.1:8001/frontend"
user_store = UserStore()
playlist = PlayList()


@app.get('/login')
def login():
    auth_url = get_auth_url()
    return {"loginUrl": auth_url}


@app.get("/callback")
def callback(code: str):
    access_token = get_access_token(code)
    user = User(access_token)

    if user_store.get_num_of_users() < 1:
        playlist.set_manager(user)

    user_store.add_user(user)
    playlist.add_top_songs_of_user(user.get_user_top_tracks(), user.get_user_id())

    redirect_url = f"{FRONTEND_URL}?user_id={user.get_user_id()}"
    return RedirectResponse(url=redirect_url)


@app.get("/user/{user_id}")  # maybe delete
def user_data(user_id: str):
    user = user_store.get_user(user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {"user_data": user.get_user_data(), "user_top_tracks": user.get_user_top_tracks()}


@app.get("/playlist")
def get_playlist():
    return {'playlist': playlist.get_songs_dict()}


@app.post("/upvote/{track_id}")
def upvote_song(track_id):

    if track_id not in playlist.get_songs_dict():
        raise HTTPException(status_code=404, detail="Song not found")

    playlist.upvote_song(track_id)

    return {'song upvoted successfully - playlist': playlist.get_songs_dict()}


@app.get("/next_song")
def get_next_song():
    next_song, num_of_votes = playlist.get_next_song()
    return {"The next song is:": next_song, "votes": num_of_votes}


@app.post("/create_playlist")
def create_playlist_on_spotify():
    try:
        playlist.create_playlist_on_spotify()
        playlist.add_songs_to_remote_playlist()

        return {'remote playlist created': playlist.show_remote_playlist()}
    except Exception as e:
        return {'exception thrown': str(e)}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)





