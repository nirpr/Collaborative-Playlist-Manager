import User


class UserStore:
    def __init__(self):
        self.__users_dict = {}

    def get_user(self, user_id):
        return self.__users_dict.get(user_id)

    def add_user(self, user):
        self.__users_dict[user.user_id] = user

    def get_num_of_user(self):
        return len(self.__users_dict)

