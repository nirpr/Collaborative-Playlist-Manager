import spotipy


class User:
    def __init__(self, user_id, access_token):
        self.user_id = user_id
        self.access_token = access_token
        self.sp = spotipy.Spotify(auth=self.access_token)

    def get_user_data(self):
        return self.sp.current_user()

