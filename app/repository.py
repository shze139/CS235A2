import json
import math

class MoviesRepository:
    def __init__(self):
        with open('./movies.json', encoding='utf-8') as file:
            self.movies = json.load(file)

    def search(self, key, by='all', page=1, size=15):
        key = key.lower()
        data = []
        for movie in self.movies:
            title = movie.get('Title', '').lower()
            actors = movie.get('Actors', '').lower()
            genre = movie.get('Genre', '').lower()
            director = movie.get('Director', '').lower()
            match = False
            if key in title and by == 'all':
                match = True
            if key in actors and (by == 'all' or by == 'actor'):
                match = True
            if key in genre and (by == 'all' or by == 'genre'):
                match = True
            if key in director and (by == 'all' or by == 'director'):
                match = True
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

    def find_by_id(self, id):
        for movie in self.movies:
            if movie.get('imdbID') == id:
                return movie

class UsersRepository:
    def __init__(self):
        self.users = []

    def add_user(self, username, password):
        self.users.append({
            'username': username,
            'password': password
        })

    def find_by_username(self, username):
        for user in self.users:
            if user.get('username') == username:
                return user

class ReviewsRepository:
    def __init__(self):
        self.reviews = []

    def add_review(self, review):
        self.reviews.append(review)

    def find_by_movieId(self, movieId):
        reviews = []
        for review in self.reviews:
            if review.get('imdbID') == movieId:
                reviews.append(review)
        return reviews

class WatchListRepository:
    def __init__(self):
        self.watchlist = []

    def add(self, item):
        self.watchlist.append(item)

    def remove(self, item):
        temp = None
        for item1 in self.watchlist:
            if item.get('username') == item1.get('username') and item.get('imdbID') == item1.get('imdbID'):
                temp = item1
        if temp:
            self.watchlist.remove(temp)

    def find_by_username(self, username):
        data = []
        for item in self.watchlist:
            if item.get('username') == username:
                data.append(item)
        return data

    def has_watch(self, username, imdbID):
        for item in self.watchlist:
            if item['username'] == username and item['imdbID'] == imdbID:
                return True
        return False
