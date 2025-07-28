from myshelf.cover import Cover
import os


def test_cover():
    cover = Cover(9780618968633, "tests/data")
    assert cover.isbn == 9780618968633
    assert cover.filename == "tests/data/9780618968633.jpg"
    assert cover.url == "https://covers.openlibrary.org/b/isbn/9780618968633-M.jpg"
    cover.fetch()
    assert os.path.exists(cover.filename)
