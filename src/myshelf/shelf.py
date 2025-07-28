from myshelf.book import Book, load_book_file
import os
from .logging_config import get_logger

logger = get_logger(__name__)


class Shelf:
    def __init__(self, name: str, directory: str):
        self.name = name
        self.books = {}
        self.directory = directory
        logger.info(f"Initializing shelf '{name}' with directory: {directory}")
        if not os.path.exists(self.directory):
            logger.error(f"Directory {self.directory} does not exist")
            raise FileNotFoundError(f"Directory {self.directory} does not exist")
        self.load_books()

    def load_books(self):
        logger.info(f"Loading books from directory: {self.directory}")
        book_count = 0

        for book_file in os.listdir(self.directory):
            if book_file.endswith(".md"):
                try:
                    logger.debug(f"Loading book from file: {book_file}")
                    book = load_book_file(
                        os.path.join(self.directory, book_file),
                        directory=self.directory,
                    )
                    self.add_book(book)
                    book_count += 1

                except Exception as e:
                    logger.error(f"Error loading book {book_file}: {e}")

        logger.info(f"Successfully loaded {book_count} books into shelf '{self.name}'")

    def add_book(self, book: Book):
        book_id = len(self.books)
        self.books[book_id] = book
        logger.debug(
            f"Added book '{book.title}' to shelf '{self.name}' with ID {book_id}"
        )

    def get_books(self):
        logger.debug(f"Retrieving {len(self.books)} books from shelf '{self.name}'")
        return self.books

    def fetch_covers(self):
        logger.info(
            f"Retrieving covers for {len(self.books)} books from shelf '{self.name}'"
        )
        for book in self.books.values():
            book.fetch_cover()
        logger.info(
            f"Successfully retrieved covers for {len(self.books)} books from shelf '{self.name}'"
        )
