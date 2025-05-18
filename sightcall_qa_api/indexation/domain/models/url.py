class Url:
    def __init__(self, value: str):
        self._value = value

    @property
    def value(self) -> str:
        return self._value

    def __str__(self):
        return self._value

    def __eq__(self, other):
        if not isinstance(other, Url):
            return NotImplemented
        return self._value == other._value

    def __hash__(self):
        return hash(self._value)
