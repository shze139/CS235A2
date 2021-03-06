
class Actor:
    def __init__(self, full_name: str):
        self._full_name = full_name

    @property
    def full_name(self) -> str:
        return self._full_name

    def __eq__(self, other):
        if not isinstance(other, Actor):
            return False
        return (
            self._full_name == other._full_name
        )