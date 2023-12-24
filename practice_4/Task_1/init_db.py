"""
CREATE TABLE Books (
    id             INTEGER    PRIMARY KEY AUTOINCREMENT,
    title          TEXT (256),
    author         TEXT (256),
    genre          TEXT (256),
    pages          INTEGER,
    published_year INTEGER,
    isbn           TEXT (256),
    rating         REAL,
    views          INTEGER
);
"""