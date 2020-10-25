class User:
    def __init__(self, username:str, password:str):
        self._username = username
        self._password = password

    @property
    def username(self) -> str:
        return self._username

    @property
    def password(self) -> str:
        return self._password

    def __eq__(self, other):
        if not isinstance(other, User):
            return False
        return (
            self._username == other._username
        )
