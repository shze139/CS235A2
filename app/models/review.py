from datetime import datetime

class Review:
    def __init__(self, content: str,  timestamp:datetime, username:str, movieId:int):
        self._content = content
        self._timestamp = timestamp
        self._username = username
        self._movieId = movieId

    @property
    def content(self) -> str:
        return self._content

    @property
    def timestamp(self) -> datetime:
        return self._timestamp.strftime('%Y-%m-%d %H:%M:%S')

    @property
    def username(self) -> str:
        return self._username

    @property
    def movieId(self) -> int:
        return self._movieId


