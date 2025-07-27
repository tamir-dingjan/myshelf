from myshelf.book import Book, load_book_file
import os

class Shelf:
    def __init__(self, name: str, directory: str):
        self.name = name
        self.books = {}
        self.directory = directory
        if not os.path.exists(self.directory):
            raise FileNotFoundError(f"Directory {self.directory} does not exist")
        self.load_books()

    def load_books(self):
        
        for book_file in os.listdir(self.directory):
            if book_file.endswith(".md"):
                try:
                    book = load_book_file(os.path.join(self.directory, book_file))
                    self.add_book(book)
                    
                except Exception as e:
                    print(f"Error loading book {book_file}: {e}")
    
    def add_book(self, book: Book):
        self.books[len(self.books)] = book

    def get_books(self):
        return self.books