from myshelf.shelf import Shelf, Book
from myshelf.logging_config import setup_logging, get_logger
import datetime
import os

setup_logging(log_file="test_shelf.log", log_level="DEBUG")
logger = get_logger(__name__)


def test_shelf_load_multuple_books():
    logger.info("Testing shelf load multiple books")
    shelf = Shelf("test", "tests/data")
    assert shelf.name == "test"
    assert shelf.directory == "tests/data"
    assert len(shelf.books) == 2
    assert shelf.books[0].title == "Sunrise on the Reaping"
    assert shelf.books[0].author == ["Suzanne Collins"]
    assert shelf.books[0].published == datetime.date(2025, 3, 18)
    assert shelf.books[1].title == "The Hobbit"
    assert shelf.books[1].author == ["J. R. R. Tolkien"]
    assert shelf.books[1].published == datetime.date(1937, 9, 21)


def test_shelf_add_book():
    logger.info("Testing shelf add book")
    shelf = Shelf("test", "tests/data")
    shelf.add_book(Book("The Hobbit", ["J. R. R. Tolkien"], datetime.date(1937, 9, 21)))
    assert len(shelf.books) == 3
    assert shelf.books[2].title == "The Hobbit"
    assert shelf.books[2].author == ["J. R. R. Tolkien"]
    assert shelf.books[2].published == datetime.date(1937, 9, 21)


def test_shelf_get_books():
    logger.info("Testing shelf get books")
    shelf = Shelf("test", "tests/data")
    assert len(shelf.get_books()) == 2
    assert shelf.get_books()[0].title == "Sunrise on the Reaping"
    assert shelf.get_books()[0].author == ["Suzanne Collins"]
    assert shelf.get_books()[0].published == datetime.date(2025, 3, 18)


def test_shelf_fetch_multiple_covers():
    logger.info("Testing shelf get multiple covers")
    shelf = Shelf("test", "tests/data")
    shelf.fetch_covers()
    for book in shelf.books.values():
        assert book.cover is not None
        assert os.path.exists(book.cover.filename)
