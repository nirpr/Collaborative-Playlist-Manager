import spotipy


class User:
    def __init__(self, user_id, access_token):
        self.__user_id = user_id
        self.__access_token = access_token
        self.__sp = spotipy.Spotify(auth=self.__access_token)
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

    def __fetch_user_top_tracks_api(self, limit=10):
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

