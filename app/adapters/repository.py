import abc
from typing import List
from datetime import date

from ..models.movie import Movie
from ..models.user import User


repo_instance = None

class RepositoryException(Exception):

    def __init__(self, message=None):
        pass


class AbstractRepository(abc.ABC):

    @abc.abstractmethod
    def add_user(self, user: User):
        """" Adds a User to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_user(self, username) -> User:
        """ Returns the User named username from the repository.

        If there is no User with the given username, this method returns None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_moivie(self, movie: Movie):
        """ Adds an movie to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movie(self, id: int) -> Movie:
        """ Returns movie with id from the repository.

        If there is no movie with the given id, this method returns None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def search_movies(self, key:str, by:str, page:int = 1, size:int = 15) -> List[Movie]:
        """ Returns a list of movies."""
        raise NotImplementedError
