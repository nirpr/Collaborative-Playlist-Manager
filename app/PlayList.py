from app.User import User
from collections import OrderedDict

class PlayList:
    def __init__(self):
        self.__songs = {}
        self.__manager = None
        self.__playlist_id = None

    def get_songs_dict(self):
        self.__reorder_by_votes()
        return self.__songs

    def get_songs_list(self):  # will use later for printing nicely
        return list(self.__songs.values())

    def __add_song(self, track, user_id):
        if track['id'] not in self.__songs:
            self.__songs[track['id']] = {'name': track['name'],
                                         'artist': track['artist'],
                                         'user_id': user_id,
                                         'votes': 0}

    def __reorder_by_votes(self):
        self.__songs = OrderedDict(sorted(self.__songs.items(), key=lambda item: item[1]['votes'], reverse=True))

    def add_user_songs_to_playlist(self, track_lst, user_id):
        for track in track_lst:
            self.__add_song(track, user_id)

    def upvote_song(self, track_id):
        if track_id in self.__songs:
            self.__songs[track_id]['votes'] += 1

    def get_next_song(self):
        if not self.__songs:
            return None

        highest_voted = max(self.__songs, key=lambda track: self.__songs[track]['votes'])
        num_of_votes = self.__songs[highest_voted]['votes']

        return highest_voted, num_of_votes

    def get_manager(self):
        return self.__manager

    def set_manager(self, user: User):
        self.__manager = user

    def create_playlist_on_spotify(self):
        if self.__manager and not self.__playlist_id:
            self.__playlist_id = self.__manager.create_playlist_in_manager()
            self.add_songs_to_remote_playlist()
            self.__delete_songs_after_remote_update()
        else:
            raise Exception({"message": "playlist already exists"})

    def add_songs_to_remote_playlist(self):
        if self.__playlist_id and self.__songs:
            self.__manager.add_songs_in_manager(self.__playlist_id, self.__songs)  # handle errors
        else:
            raise Exception({"message": "playlist does not exists"})

    def __delete_songs_after_remote_update(self):
        self.__songs = {}

    def show_remote_playlist(self):
        return self.__manager.show_remote_playlist(self.__playlist_id)

