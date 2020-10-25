
class Director:

    def __init__(self, full_name: str):
        self._full_name = full_name

    @property
    def full_name(self) -> str:
        return self._full_name

