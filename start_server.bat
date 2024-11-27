@echo off

call conda activate collaborative_playlist

cd C:\Users\nirpe\PycharmProjects\spotify_shared_playlist_by_votes

uvicorn main:app --reload