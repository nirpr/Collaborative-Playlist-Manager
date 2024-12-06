import spotipy
# from app.PlayList import PlayList


class User:
    def __init__(self, access_token):
        self.__access_token = access_token
        self.__sp = spotipy.Spotify(auth=self.__access_token, requests_session=False)
        self.__user_id = self.__sp.me()['id']
        self.__user_data = self.__fetch_user_data_api()
        self.__user_top_tracks = self.__fetch_user_top_tracks_api()

    def get_user_data(self):
        return self.__user_data

    def get_user_top_tracks(self):
        return self.__user_top_tracks

    def get_user_id(self):
        return self.__user_id

    def __fetch_user_data_api(self):
        return self.__sp.current_user()

    def __fetch_user_top_tracks_api(self, limit=20):
        try:
            response = self.__sp.current_user_top_tracks(limit)
            tracks = [{"name": item["name"],
                       "artist": item["artists"][0]["name"],
                       "id": item["id"]}
                      for item in response['items']]

            return tracks
        except spotipy.exceptions.SpotifyException as e:
            print(f"Spotify API error: {e}")
            return []
        except Exception as e:
            print(f"Error fetching top tracks: {e}")
            return []

    def create_playlist_in_manager(self):
        created_playlist = self.__sp.user_playlist_create(self.__user_id,
                                                          name="Collaborative Playlist",
                                                          public=True)  # maybe change param

        return created_playlist['id']

    def add_songs_in_manager(self, playlist_id, songs):
        self.__sp.playlist_add_items(playlist_id, songs)

    def show_remote_playlist(self, playlist_id):
        playlist_details = self.__sp.playlist(playlist_id)

        playlist_info = {
            "name": playlist_details["name"],
            "description": playlist_details["description"],
            "tracks": [
                {
                    "name": track["track"]["name"],
                    "artist": track["track"]["artists"][0]["name"]
                }
                for track in playlist_details["tracks"]["items"]
            ],
        }
        return playlist_info
