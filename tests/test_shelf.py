from myshelf.shelf import Shelf
import datetime

def test_shelf():
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