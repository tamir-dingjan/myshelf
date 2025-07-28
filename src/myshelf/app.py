from flask import Flask
from markupsafe import escape
from .logging_config import get_logger

logger = get_logger(__name__)

app = Flask(__name__)


@app.route("/")
def index():
    logger.info("Index page accessed")
    return "<p>This is the index page</p>"


@app.route("/shelf")
def show_shelf(shelf):
    # Show all the books
    logger.info(f"Shelf page accessed for shelf: {shelf}")
    return "<p>This is the shelf page</p>"


@app.route("/book/<int:book_id>")
def show_book(book_id):
    # Show a single book
    logger.info(f"Book page accessed for book ID: {book_id}")
    return f"<p>This is a page for a single book with id {escape(book_id)}</p>"
