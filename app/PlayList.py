

class PlayList:
    def __init__(self):
        self.__songs = {}

    def get_songs_dict(self):
        return self.__songs

    def __add_song(self, track_id, user_id):
        if track_id not in self.__songs:
            self.__songs[track_id] = {'user_id': user_id, 'votes': 0}

    def add_top_songs_of_user(self, track_lst, user_id):
        for track in track_lst:
            self.__add_song(track['id'], user_id)

    def upvote_song(self, track_id):
        if track_id in self.__songs:
            self.__songs[track_id]['votes'] += 1

    def get_next_song(self):
        if not self.__songs:
            return None

        highest_voted = max(self.__songs, key=lambda track: self.__songs[track]['votes'])
        num_of_votes = self.__songs[highest_voted]['votes']

        return highest_voted, num_of_votes


