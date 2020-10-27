from typing import List

class WatchList:
    def __init__(self):
        self._watchlist: List = list()

    @property
    def list(self) -> List:
        return self._watchlist

    def add_watch(self, username:str, movieId:int):
        self._watchlist.append((username, movieId))

    def remove_watch(self, username:str, movieId:int):
        for item in self._watchlist:
            if username == item[0] and movieId == item[1]:
                self._watchlist.remove(item)
                break

    def has_watch(self, username:str, movieId:int):
        for username1,movieId1 in self._watchlist:
            if username1 == username and movieId1 == movieId:
                return True
        return False
