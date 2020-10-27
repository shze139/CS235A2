import csv
import os
import math
from datetime import date, datetime
from typing import List

from bisect import bisect, bisect_left, insort_left

from werkzeug.security import generate_password_hash
from .repository import AbstractRepository

from ..models.movie import Movie
from ..models.genre import Genre
from ..models.director import Director
from ..models.actor import Actor
from ..models.user import User
from ..models.watchlist import WatchList
from ..models.review import Review


class MemoryRepository(AbstractRepository):
    def __init__(self):
        self._movies:List[Movie] = list()
        self._users:List[User] = list()
        self._watchlist:WatchList = WatchList()
        self._reviews:List[Review] = list()

    def add_user(self, user: User):
        self._users.append(user)

    def get_user(self, username) -> User:
        return next((user for user in self._users if user.username == username), None)

    def add_moivie(self, movie: Movie):
        self._movies.append(movie)

    def get_movie(self, id):
        for movie in self._movies:
            if movie.id == id:
                return movie

    def search_movies(self, key:str, by:str, page:int = 1, size:int = 50):
        key = key.lower()
        data = []
        for movie in self._movies:
            title = movie.title.lower()
            actors = movie.actors
            genre = movie.genre
            director = movie.director
            match = False
            if key in title and by == 'all':
                match = True
            if by == 'actor' or by == 'all':
                for actor in actors:
                    if key in actor.full_name.lower():
                        match = True
                        break
            if by == 'genre' or by == 'all':
                for action in genre:
                    if key in action.name.lower():
                        match = True
                        break
            if by == 'director' or by == 'all':
                for item in director:
                    if key in item.full_name.lower():
                        match = True
                        break
            if match:
                data.append(movie)
        start = (page - 1) * size
        end = page * size
        total = len(data)
        totalPage = math.ceil(len(data) / size)
        if start > total:
            start = total
        if end > total:
            end = total
        return {
            'movies': data[start:end],
            'total': total,
            'totalPage': totalPage,
            'page': page,
            'size': size
        }

    def add_watch(self, username:str, movieId:int):
        self._watchlist.add_watch(username, movieId)

    def has_watch(self, username:str, movieId:int):
        return self._watchlist.has_watch(username, movieId)

    def remove_watch(self, username:str, movieId:int):
        return self._watchlist.remove_watch(username, movieId)

    def add_review(self, review:Review):
        self._reviews.append(review)

    def get_reviews_by_movie_id(self, movieId:int) -> List[Review]:
        data = []
        for review in self._reviews:
            if review.movieId == movieId:
                data.append(review)
        return data

    def get_watch_movies(self, username:str):
        movies = []
        for username1,movieId in self._watchlist.list:
            if username1 == username:
                movies.append(self.get_movie(movieId))
        return movies

def load_genre(genre):
    data = []
    for item in genre.split(','):
        data.append(Genre(item))
    return data

def load_director(director):
    data = []
    for item in director.split(','):
        data.append(Director(item))
    return data

def load_actors(actors):
    data = []
    for item in actors.split(','):
        data.append(Actor(item))
    return data

def parse_float(s):
    v = None
    try:
        v = float(s)
    except ValueError:
        pass
    return v

def load_movies(data_path: str, repo: MemoryRepository):
    with open(os.path.join(data_path, 'Data1000Movies.csv'), mode='r', encoding='utf-8-sig') as csvfile:
        movie_file_reader = csv.DictReader(csvfile)

        index = 1
        for row in movie_file_reader:
            id = index
            rank = int(row['Rank'])
            title = row['Title']
            genre = load_genre(row['Genre'])
            description = row['Description']
            director = load_director(row['Director'])
            actors = load_actors(row['Actors'])
            year = int(row['Year'])
            runtime = parse_float(row['Runtime (Minutes)'])
            rating = parse_float(row['Rating'])
            votes = int(row['Votes'])
            revenue = parse_float(row['Revenue (Millions)'])
            metascore = parse_float(row['Metascore'])
            movie = Movie(id, rank, title, genre, description, director, actors, year, runtime, rating, votes, revenue, metascore)
            repo.add_moivie(movie)
            index += 1

def populate(data_path: str, repo: MemoryRepository):
    load_movies(data_path, repo)