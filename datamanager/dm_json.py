import json
from os.path import isfile
from .dm_interface import DataManagerInterface


class JSONDataManager(DataManagerInterface):
    """Data manager class which interfaces with the JSON data file"""
    def __init__(self, filename="datamanager/data.json"):
        self.filename = filename
        if not isfile(filename):
            self.save_to_file([])

    def save_to_file(self, data) -> None:
        """Saves the provided data to the json data file"""
        with open(self.filename, 'w') as file:
            file.write(json.dumps(data, indent=4))

    def get_all_users(self) -> list:
        """Returns a list of all users from data file,
        each user data as a dict object."""
        with open(self.filename, 'r') as file:
            return json.loads(file.read())

    def is_user_id_exists(self, user_id):
        """Checks if user_id exists in data file,
        Returns boolean value accordingly"""
        for user in self.get_all_users():
            if user['id'] == user_id:
                return True
        return False

    def add_user(self, user_dict) -> None:
        """Adds a new user to data file"""
        users_list = self.get_all_users()
        user_ids = (user['id'] for user in users_list)
        if user_dict['id'] not in user_ids:
            users_list.append(user_dict)
            self.save_to_file(users_list)

    def delete_user(self, user_id) -> None:
        """Deletes a user from data file"""
        users_list = self.get_all_users()
        for user in users_list:
            if user['id'] == user_id:
                users_list.remove(user)
        self.save_to_file(users_list)

    def update_user(self, user_id, update_dict) -> None:
        """Update user data in data file"""
        users_list = self.get_all_users()
        for user in users_list:
            if user['id'] == user_id:
                user.update(update_dict)
        self.save_to_file(users_list)

    def get_user(self, user_id) -> dict:
        """Returns a user dict based on user_id"""
        users_list = self.get_all_users()
        for user in users_list:
            if user['id'] == user_id:
                return user

    def get_user_movies(self, user_id) -> list:
        """Returns a list of user movies based on input user_id,
        each movie data as a dict object."""
        return self.get_user(user_id)['movies']

    def get_user_single_movie(self, user_id, movie_id) -> dict:
        """Returns a dictionary with the specific user movie"""
        user_movies = self.get_user_movies(user_id)
        for movie in user_movies:
            if movie['id'] == movie_id:
                return movie

    def add_user_movie(self, user_id, movie_dict) -> None:
        """Adds a new movie to specific user in data file"""
        users_list = self.get_all_users()
        for user in users_list:
            if user['id'] == user_id:
                movie_names = (movie['name'] for movie in user['movies'])
                if movie_dict['name'] not in movie_names:
                    user['movies'].append(movie_dict)
                else:
                    raise ValueError("Movie already exists, try again")
        self.save_to_file(users_list)

    def is_movie_id_exists(self, user_id, movie_id) -> bool:
        """Checks if movie_id exists in users movies list,
        Returns boolean value accordingly"""
        for movie in self.get_user_movies(user_id):
            if movie['id'] == movie_id:
                return True
        return False

    def delete_user_movie(self, user_id, movie_id) -> None:
        """Deletes a movie from specific user in data file"""
        users_list = self.get_all_users()
        for user in users_list:
            if user['id'] == user_id:
                for movie in user['movies']:
                    if movie['id'] == movie_id:
                        user['movies'].remove(movie)
        self.save_to_file(users_list)

    def update_user_movie(self, user_id, movie_id, update_dict) -> None:
        """Update a movie from specific user in data file"""
        users_list = self.get_all_users()
        for user in users_list:
            if user['id'] == user_id:
                for movie in user['movies']:
                    if movie['id'] == movie_id:
                        movie.update(update_dict)
                        if not update_dict.get('note'):
                            del movie['note']
        self.save_to_file(users_list)
