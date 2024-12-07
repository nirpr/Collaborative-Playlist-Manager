from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.auth import get_auth_url, get_access_token
from app.User import User
from app.User_store import UserStore
from app.PlayList import PlayList
from fastapi.responses import RedirectResponse
from random import sample

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
    # return {"loginUrl": auth_url}
    return RedirectResponse(url=auth_url)


@app.get("/callback")
def callback(code: str):
    access_token = get_access_token(code)
    user = User(access_token)

    if user_store.get_num_of_users() < 1:
        playlist.set_manager(user)

    user_store.add_user(user)

    # redirect_url = f"{FRONTEND_URL}?user_id={user.get_user_id()}"
    # return RedirectResponse(url=redirect_url)
    return {"successfully logged in": user.get_user_id()}


@app.get("/playlist")
def get_playlist():
    return {'playlist': playlist.get_songs_dict()}


@app.get("/next_song")
def get_next_song():
    next_song, num_of_votes = playlist.get_next_song()
    return {"The next song is:": next_song, "votes": num_of_votes}


@app.post("/generate_playlist")
def generate_playlist():
    num_of_songs_per_user = 10 // user_store.get_num_of_users()

    if user_store.get_num_of_users() > 10:
        selected_users = sample(list(user_store.get_users_dict().values()), 10)
    else:
        selected_users = list(user_store.get_users_dict().values())

    for user in selected_users:
        if len(user.get_user_top_tracks()) < num_of_songs_per_user:
            num_of_songs_per_user = len(user.get_user_top_tracks())
        selected_songs = sample(user.get_user_top_tracks(), num_of_songs_per_user)
        playlist.add_user_songs_to_playlist(selected_songs, user.get_user_id())

    return {'selected playlist': playlist.get_songs_dict()}


@app.post("/upvote/{track_id}")
def upvote_song(track_id):

    if track_id not in playlist.get_songs_dict():
        raise HTTPException(status_code=404, detail="Song not found")

    playlist.upvote_song(track_id)

    return {'song upvoted successfully - playlist': playlist.get_songs_dict()}


@app.post("/create_playlist")
def create_playlist_on_spotify():
    try:
        playlist.create_playlist_on_spotify()
        return {'remote playlist created': playlist.show_remote_playlist()}
    except Exception as e:
        return {'exception thrown': str(e)}


@app.post("/add_songs_to_playlist")
def add_songs_to_playlist():
    try:
        playlist.add_songs_to_remote_playlist()
    except Exception as e:
        return {'exception thrown': str(e)}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)





