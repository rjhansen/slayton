from pathlib import Path

import pytest

import slayton
from slayton import parse
from slayton.errors import (
    DuplicateCityError,
    JaggedRowError,
    NonZeroSelfDistanceError,
    NotSquareError,
    NotSymmetricError,
    OutOfOrderError,
    TableError,
)

TESTBED_PATH = Path(slayton.__file__).resolve().parent / "testbed.txt"


def test_valid_two_city_table():
    text = '"Atlanta" 0 936\n"Boston" 936 0\n'
    error, table = parse(text)
    assert error is None
    assert table == {"Atlanta": [0.0, 936.0], "Boston": [936.0, 0.0]}


def test_valid_single_city_table():
    error, table = parse('"Atlanta" 0\n')
    assert error is None
    assert table == {"Atlanta": [0.0]}


def test_valid_table_with_commas_and_single_quotes():
    text = "'Atlanta' 0, 936\n'Boston' 936, 0\n"
    error, table = parse(text)
    assert error is None
    assert table == {"Atlanta": [0.0, 936.0], "Boston": [936.0, 0.0]}


def test_valid_table_with_decimal_distances():
    text = '"Atlanta" 0.0 5.5\n"Boston" 5.5 0.0\n'
    error, table = parse(text)
    assert error is None
    assert table == {"Atlanta": [0.0, 5.5], "Boston": [5.5, 0.0]}


def test_testbed_file_parses_successfully():
    error, table = parse(TESTBED_PATH.read_text())
    assert error is None
    assert set(table.keys()) == {
        "Atlanta",
        "Boston",
        "Chicago",
        "Denver",
        "El Paso",
        "Fort Worth",
    }
    for city, row in table.items():
        assert len(row) == len(table)
        assert row[list(table).index(city)] == 0.0


def test_empty_input_is_syntax_error():
    error, table = parse("")
    assert isinstance(error, SyntaxError)
    assert table == {}


@pytest.mark.parametrize(
    ("text", "expected_type"),
    [
        pytest.param(
            '"Atlanta" 0 1\n"Atlanta" 1 0\n',
            DuplicateCityError,
            id="duplicate-city",
        ),
        pytest.param(
            '"Boston" 0 1\n"Atlanta" 1 0\n',
            OutOfOrderError,
            id="out-of-order",
        ),
        pytest.param(
            '"Atlanta" 0 1\n"Boston" 1 0 5\n',
            JaggedRowError,
            id="jagged-row",
        ),
        pytest.param(
            '"Atlanta" 0 5\n"Boston" 5 0\n"Chicago" 9 9\n',
            NotSquareError,
            id="not-square-too-many-rows",
        ),
        pytest.param(
            '"Atlanta" 0 5 9\n"Boston" 5 0 9\n',
            NotSquareError,
            id="not-square-too-few-rows",
        ),
        pytest.param(
            '"Atlanta" 0 5\n"Boston" 6 0\n',
            NotSymmetricError,
            id="not-symmetric",
        ),
        pytest.param(
            '"Atlanta" 1 5\n"Boston" 5 0\n',
            NonZeroSelfDistanceError,
            id="nonzero-self-distance",
        ),
    ],
)
def test_table_error_paths(text, expected_type):
    error, table = parse(text)
    assert isinstance(error, expected_type)
    assert isinstance(error, TableError)
    assert table == {}


@pytest.mark.parametrize(
    "text",
    [
        pytest.param('"Atlanta 0 1\n"Boston" 1 0\n', id="unterminated-string"),
        pytest.param(
            '"Atlanta" 0 -5\n"Boston" -5 0\n',
            id="negative-number-not-allowed-by-grammar",
        ),
        pytest.param("@@@ not a table at all @@@", id="garbage-input"),
    ],
)
def test_syntax_error_paths(text):
    error, table = parse(text)
    assert isinstance(error, SyntaxError)
    assert not isinstance(error, TableError)
    assert table == {}


def test_table_error_message_includes_location():
    error, _ = parse('"Atlanta" 0 1\n"Atlanta" 1 0\n')
    assert isinstance(error, DuplicateCityError)
    assert "line 2:0" in str(error)
    assert "Atlanta" in str(error)
