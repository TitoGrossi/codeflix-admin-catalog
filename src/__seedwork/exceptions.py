class InvalidUUIDException(Exception):
    def __init__(self, error: str = "ID must be valid UUID") -> None:
        super().__init__(error)
