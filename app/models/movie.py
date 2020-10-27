from typing import List
from .genre import Genre
from .actor import Actor
from .director import Director
import requests

class Movie:
    def __init__(self, id:int, rank: int, title: str,
                 genre: List[Genre], description: str, director: List[Director],
                 actors: List[Actor], year: int, runtime: float,
                 rating: float,votes: int, revenue:float, metascore:int):
        self._id = id
        self._rank = rank
        self._title = title
        self._genre = genre
        self._description = description
        self._director = director
        self._actors = actors
        self._year = year
        self._runtime = runtime
        self._rating = rating
        self._votes = votes
        self._revenue = revenue
        self._metascore = metascore
        self._poster = None

    @property
    def id(self) -> int:
        return self._id

    @property
    def rank(self) -> int:
        return self._rank

    @property
    def title(self) -> str:
        return self._title

    @property
    def genre(self) -> List[Genre]:
        return self._genre

    @property
    def description(self) -> str:
        return self._description

    @property
    def director(self) -> List[Director]:
        return self._director

    @property
    def actors(self) -> List[Actor]:
        return self._actors

    @property
    def year(self) -> int:
        return self._year

    @property
    def runtime(self) -> float:
        return self._runtime

    @property
    def rating(self) -> float:
        return self._rating

    @property
    def votes(self) -> int:
        return self._votes

    @property
    def revenue(self) -> float:
        return self._revenue

    @property
    def metascore(self) -> float:
        return self._metascore

    @property
    def poster(self) -> str:
        if not self._poster:
            try:
                res = requests.get('http://www.omdbapi.com', params={
                    't': self._title,
                    'y': self._year,
                    'type': 'movie',
                    'apikey': '52c4f1cd'
                })
                data = res.json()
                if data.get('Response'):
                    self._poster = data.get('Poster')
            except:
                pass
        return self._poster

    def __eq__(self, other):
        if not isinstance(other, Movie):
            return False
        return self._id == other._id


