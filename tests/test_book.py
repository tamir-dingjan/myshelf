from myshelf.book import load_book_file
from myshelf.logging_config import setup_logging, get_logger
import datetime, os

setup_logging(log_file="test_book.log", log_level="DEBUG")
logger = get_logger(__name__)


def test_load_book_file():
    logger.info("Testing load_book_file")
    book = load_book_file("tests/data/Sunrise on the Reaping.md")
    assert book.title == "Sunrise on the Reaping"
    assert book.author == ["Suzanne Collins"]
    assert book.published == datetime.date(2025, 3, 18)
    assert book.properties == {
        "cover": "https://upload.wikimedia.org/wikipedia/en/2/20/Sunrise_on_the_Reaping_book_cover.jpg",
        "tags": ["young-adult", "dystopian", "science-fiction", "fiction"],
        "rating": 3.5,
        "pages": 400,
        "lists": ["2025 Reads", "Hunger Games"],
        "comment": "Good, but not as riveting as the original series",
    }


def test_fetch_isbn():
    logger.info("Testing fetch_isbn")
    book = load_book_file("tests/data/Sunrise on the Reaping.md")
    book.fetch_isbn()
    assert book.get_property("isbn") == "1546171460"


def test_fetch_cover():
    logger.info("Testing fetch_cover")
    book = load_book_file(
        "tests/data/Sunrise on the Reaping.md", directory="tests/data"
    )
    book.fetch_cover()
    assert book.cover is not None
    assert os.path.exists(book.cover.filename)
