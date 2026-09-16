=======
slayton
=======

In 2006, I mentored an undergraduate (whose last name was “Slayton”) in the
art of writing reliable software that met professional standards. We used a
toy problem from his homework — parsing a labeled adjacency matrix.

In 2026 I got bored and decided to repeat the exercise, showing current
Python best practices and how complex things become the moment you commit
to doing them Thoroughly Right.

Usage
=====

The library exposes a single public function, ``slayton.parse``, for reading
a labeled adjacency matrix — a table of the pairwise distances between a
set of named cities — out of plain text.

.. code-block:: python

    from slayton import parse

    text = '''
    "Atlanta"    0  936  588
    "Boston"   936    0  850
    "Chicago"  588  850    0
    '''

    error, table = parse(text)
    if error is not None:
        raise error
    print(table["Atlanta"])  # [0.0, 936.0, 588.0]

``parse(input: str) -> tuple[Exception | None, dict[str, list[float]]]``
    Parses ``input`` as a table of city names, each followed by its distance
    to every city in the table, itself included. Each row begins with a
    quoted city name and continues with one number per city, separated by
    optional commas and/or whitespace.

    Rather than raising, ``parse`` returns an ``(error, table)`` pair:

    - On success, ``error`` is ``None`` and ``table`` maps each city name to
      its row of distances, in the order the columns appeared in ``input``.
    - On failure, ``error`` holds the exception describing what went wrong,
      and ``table`` is an empty dict.

    ``parse`` only accepts input describing a well-formed distance matrix,
    rejecting — each with its own exception — a table that:

    - is not syntactically valid (``SyntaxError``);
    - lists a city more than once (``DuplicateCityError``);
    - lists its cities out of lexicographic order (``OutOfOrderError``);
    - has rows of differing lengths (``JaggedRowError``);
    - isn't square, i.e. the number of distances per row doesn't match the
      number of rows (``NotSquareError``);
    - gives a city a non-zero distance to itself (``NonZeroSelfDistanceError``);
    - isn't symmetric, i.e. city A's distance to city B doesn't match city
      B's distance to city A (``NotSymmetricError``).

    All of these exceptions are defined in ``slayton.errors`` and subclass
    ``TableError``.
