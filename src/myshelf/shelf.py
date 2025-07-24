from myshelf.book import Book

class Shelf:
    def __init__(self, name: str):
        self.name = name
        self.books = []

    def add_book(self, book: Book):
        self.books.append(book)

    def get_books(self):
        return self.books