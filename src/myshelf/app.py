from flask import Flask
from markupsafe import escape

app = Flask(__name__)

@app.route('/')
def index():
    return "<p>This is the index page</p>"

@app.route('/shelf')
def show_shelf(shelf):
    # Show all the books
    return "<p>This is the shelf page</p>"

@app.route('/book/<int:book_id>')
def show_book(book_id):
    # Show a single book
    return f"<p>This is a page for a single book with id {escape(book_id)}</p>"
