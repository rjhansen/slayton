from antlr4 import Token


class TableError(Exception):
    """Base class for semantic errors in an otherwise syntactically valid table."""

    def __init__(self, message: str, token: Token | None = None) -> None:
        if token is not None:
            message = f"line {token.line}:{token.column} {message}"
        super().__init__(message)
        self.token = token


class DuplicateCityError(TableError):
    pass


class OutOfOrderError(TableError):
    pass


class JaggedRowError(TableError):
    pass


class NonZeroSelfDistanceError(TableError):
    pass


class NegativeDistanceError(TableError):
    pass


class NotSquareError(TableError):
    pass


class NotSymmetricError(TableError):
    pass
