
"""
CREATE TABLE books (
    id             INTEGER    PRIMARY KEY AUTOINCREMENT,
    title          TEXT (256),
    author         TEXT (256),
    genre          TEXT (256),
    pages          INTEGER,
    published_year INTEGER,
    isbn           TEXT (256),
    rating         REAL,
    views          INTEGER,
    price          INTEGER,
    place          INTEGER,
    date           INTEGER
);
"""

"""
CREATE TABLE sales (
    id       INTEGER    PRIMARY KEY AUTOINCREMENT,
    books_id INTEGER,
    price    INTEGER,
    place    TEXT (256),
    date     TEXT (256) 
);

"""