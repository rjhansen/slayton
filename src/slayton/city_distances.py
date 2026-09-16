#!/usr/bin/env python3

from pathlib import Path
from typing import TYPE_CHECKING, override

from antlr4 import (
    CommonTokenStream,
    InputStream,
    ParseTreeWalker,
    RecognitionException,
    Token,
)
from antlr4.error.ErrorListener import ErrorListener
from antlr4.Recognizer import Recognizer
from antlr4.tree.Tree import TerminalNodeImpl

if TYPE_CHECKING:
    # Static analyzers (pyright, etc.) can't evaluate the `"." in __name__`
    # runtime check below, so give them a single, always-resolvable import
    # to type against. This block never runs.
    from .CityDistancesLexer import CityDistancesLexer
    from .CityDistancesListener import CityDistancesListener
    from .CityDistancesParser import CityDistancesParser
    from .errors import (
        DuplicateCityError,
        JaggedRowError,
        NegativeDistanceError,
        NonZeroSelfDistanceError,
        NotSquareError,
        NotSymmetricError,
        OutOfOrderError,
        TableError,
    )
elif "." in __name__:
    from .CityDistancesLexer import CityDistancesLexer
    from .CityDistancesListener import CityDistancesListener
    from .CityDistancesParser import CityDistancesParser
    from .errors import (
        DuplicateCityError,
        JaggedRowError,
        NegativeDistanceError,
        NonZeroSelfDistanceError,
        NotSquareError,
        NotSymmetricError,
        OutOfOrderError,
        TableError,
    )
else:
    from CityDistancesLexer import CityDistancesLexer
    from CityDistancesListener import CityDistancesListener
    from CityDistancesParser import CityDistancesParser
    from errors import (
        DuplicateCityError,
        JaggedRowError,
        NegativeDistanceError,
        NonZeroSelfDistanceError,
        NotSquareError,
        NotSymmetricError,
        OutOfOrderError,
        TableError,
    )


class RaisingErrorListener(ErrorListener):
    @override
    def syntaxError(
        self,
        recognizer: Recognizer,
        offendingSymbol: Token | None,
        line: int,
        column: int,
        msg: str,
        e: RecognitionException | None,
    ) -> None:
        raise SyntaxError(f"line {line}:{column} {msg}")


class MyListener(CityDistancesListener):
    def __init__(self) -> None:
        self.table: dict[str, list[float]] = {}
        self.row_count: int = 0
        self.last_city: str = ""
        self.cities: int = 0

    @override
    def enterRow(self, ctx: CityDistancesParser.RowContext) -> None:
        city_ctx = ctx.city()
        assert city_ctx is not None
        string_node = city_ctx.STRING()
        assert isinstance(string_node, TerminalNodeImpl)
        token: Token = string_node.symbol
        assert token.text is not None
        city: str = token.text[1:-1]

        if city in self.table:
            raise DuplicateCityError(f"duplicate city '{city}'", token)

        if self.row_count > 0 and city <= self.last_city:
            raise OutOfOrderError("table is not in lexicographical order", token)
        self.last_city = city

        numbers = ctx.NUMBER()
        assert isinstance(numbers, list)
        distances: list[float] = [float(X.getText()) for X in numbers]
        if self.row_count == 0:
            self.cities = len(distances)
        if len(distances) != self.cities:
            raise JaggedRowError(f"row for '{city}' is jagged", token)
        for index in range(len(distances)):
            if index == self.row_count and distances[self.row_count] != 0.0:
                raise NonZeroSelfDistanceError(
                    f"self-distance of '{city}' is non-zero", token
                )

            # This should never ever ever hit, because per our ANTLR grammar
            # a minus sign isn't allowed inside a NUMBER. Some will call this
            # dead code. I call it belt and suspenders engineering, on the
            # off chance the Good Idea Fairy visits the next maintainer and
            # they think "oh, omitting negative values from NUMBER must've
            # been an oversight."
            #
            # So, yeah. Dead code. Leave it in anyway. And if you're the next
            # maintainer and you're reading this, you're welcome.
            elif distances[index] < 0:
                raise NegativeDistanceError(
                    f"in '{city}', column {index} is negative", token
                )
        self.table[city] = distances
        self.row_count += 1

    def exitTable(self, ctx: CityDistancesParser.TableContext) -> None:
        # Ensure the number of columns equals the number of cities.
        cities = sorted(self.table.keys())

        # We've already guaranteed the matrix is not jagged: now we
        # ensure that it's square.

        if len(self.table[cities[0]]) != len(cities):
            raise NotSquareError("adjacency list is not square", ctx.stop)

        # A rectangular adjacency matrix is prone to data entry
        # errors, where the A->B distance is not the same as the
        # B->A distance. Let's ensure our matrix is symmetric.

        matrix: list[list[float]] = []
        for city in sorted(self.table.keys()):
            row = self.table[city]
            matrix.append(row)
        n: int = len(matrix[0])
        if not all(
            matrix[i][j] == matrix[j][i] for i in range(n) for j in range(i + 1, n)
        ):
            raise NotSymmetricError("adjacency list is not symmetric", ctx.stop)


def parse(input: str) -> tuple[Exception | None, dict[str, list[float]]]:
    """Given an input string, parse it out into an adjacency matrix where each
    row represents a distance between two cities. The details of the format can
    be found in 'CityDistances.g4', but here's a short sample:

        "Atlanta"   0  50 100
        "Boston"   50   0  75
        "Chicago" 100  75   0

    The numeric part of the data must be square and symmetric. Cities can be
    listed in either single or double quotes. Cities must be listed in strictly
    increasing lexicographical order.

    It returns a tuple of (error, data), where the error is either one of its
    specific exceptions like SyntaxError or OutOfOrderError, or else None.
    If it returns an exception, do not rely on the data having any particular
    meaning. If it runs successfully, error will be None and the data will be
    a dictionary somewhat like what follows:

        {
            "Atlanta": [0.0, 50.0, 100.0],
            "Boston": [50.0, 0.0, 75.0],
            "Chicago": [100.0, 75.0, 0.0]
        }
    """
    try:
        lexer: CityDistancesLexer = CityDistancesLexer(InputStream(input))
        lexer.removeErrorListeners()
        lexer.addErrorListener(RaisingErrorListener())

        stream: CommonTokenStream = CommonTokenStream(lexer)
        parser: CityDistancesParser = CityDistancesParser(stream)
        parser.removeErrorListeners()
        parser.addErrorListener(RaisingErrorListener())

        tree: CityDistancesParser.TableContext = parser.table()
        listener: MyListener = MyListener()
        walker: ParseTreeWalker = ParseTreeWalker()
        walker.walk(listener, tree)
        return (None, listener.table)
    except (TableError, SyntaxError) as e:
        return (e, {})


def unit_test() -> None:
    testbed = Path(__file__).parent / "testbed.txt"
    with open(testbed) as fh:
        (err, data) = parse(fh.read())
    if err is not None:
        print(f"error: {err}")
        return
    for city in data:
        print(f"{city}: {data[city]}")


if __name__ == "__main__":
    unit_test()
