class InvalidFormat(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class UnsupportedFormat(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class DuplicateKey(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
