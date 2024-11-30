from fastapi import FastAPI, HTTPException
from app.auth import get_auth_url, get_access_token
from app.User import User
from app.User_store import UserStore
from app.PlayList import PlayList
from fastapi.responses import RedirectResponse

app = FastAPI()
user_store = UserStore()
playlist = PlayList()


@app.get('/')
def login():
    auth_url = get_auth_url()
    return RedirectResponse(auth_url)


@app.get("/callback")
def callback(code: str):
    access_token = get_access_token(code)
    user = User(access_token)

    if user_store.get_num_of_users() < 1:
        playlist.set_manager(user)

    user_store.add_user(user)
    playlist.add_top_songs_of_user(user.get_user_top_tracks(), user.get_user_id())

    return RedirectResponse(url=f"/user/{user.get_user_id()}")


@app.get("/user/{user_id}")
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
        return {'exception thrown': e}







