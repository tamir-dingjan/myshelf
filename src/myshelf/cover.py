import os, requests
from .logging_config import get_logger

logger = get_logger(__name__)


class Cover:
    def __init__(self, isbn: int, directory: str):
        self.isbn = isbn
        self.directory = directory
        self.filename = os.path.join(self.directory, f"{self.isbn}.jpg")
        self.url = f"https://covers.openlibrary.org/b/isbn/{self.isbn}-M.jpg"
        logger.debug(f"Cover object created for ISBN {isbn}")

    def __repr__(self):
        return f"Cover(isbn={self.isbn}, filename={self.filename}, url={self.url})"

    def fetch(self):
        logger.info(f"Fetching cover for ISBN {self.isbn}")
        response = requests.get(self.url)
        if response.status_code == 200:
            with open(self.filename, "wb") as file:
                file.write(response.content)
            logger.info(f"Cover successfully saved to {self.filename}")
        else:
            logger.error(
                f"Failed to fetch cover for ISBN {self.isbn}, status code: {response.status_code}"
            )
