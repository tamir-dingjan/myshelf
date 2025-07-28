import yaml, datetime, shutil, os, requests
from .logging_config import get_logger
from myshelf.cover import Cover
import tempfile

logger = get_logger(__name__)


class Book:
    def __init__(
        self, title: str, author: str, published: datetime.date, directory: str = None
    ):
        self.title = title
        self.author = author
        self.published = published
        self.properties = {}
        self.cover = None
        if directory is None or not os.path.exists(directory):
            self.directory = tempfile.mkdtemp()

            # If we make a temp dir for this book, delete it when the book is deleted
            def __del__(self):
                shutil.rmtree(self.directory)

        else:
            self.directory = directory

    def __repr__(self):
        return f"Book(title={self.title}, author={self.author}, published={self.published})"

    def __str__(self):
        return f"{self.title} by {self.author} ({self.published.year})"

    def add_property(self, key: str, value: str):
        self.properties[key] = value

    def get_property(self, key: str):
        return self.properties.get(key, None)

    def get_properties(self):
        return self.properties

    def fetch_isbn(self):
        if self.get_property("isbn") is None:
            logger.info(f"Fetching ISBN for {self.__repr__()}")
            query_url = f"https://openlibrary.org/search.json?title={self.title.replace(' ', '+')}&author={self.author[0].replace(' ', '+')}&limit=2&offset=0&fields=isbn"
            response = requests.get(query_url)
            if response.status_code == 200:
                try:
                    data = response.json()
                    self.add_property("isbn", data["docs"][0]["isbn"][0])
                except Exception as e:
                    logger.error(f"Error parsing ISBN for {self.__repr__()}: {e}")
                    self.add_property("isbn", None)
            else:
                logger.error(f"Failed to fetch ISBN for {self.__repr__()}")
        else:
            logger.info(f"ISBN already exists for {self.__repr__()}")

    def fetch_cover(self):

        self.fetch_isbn()

        if self.cover is None:
            logger.info(f"Fetching cover for {self.__repr__()}")
            self.cover = Cover(self.get_property("isbn"), self.directory)
            self.cover.fetch()

        else:
            logger.info(f"Cover already exists for {self.__repr__()}")


def load_book_file(book_file: str, directory: str = None):
    """Load a book from a formatted markdown file.
    The format is based on that used in Obsidian's "Bookshelf" plugin (https://weph.github.io/obsidian-bookshelf/docs/getting-started):
    I.e., the following structure:

    ---
    title: Sunrise on the Reaping
    cover: 'https://upload.wikimedia.org/wikipedia/en/2/20/Sunrise_on_the_Reaping_book_cover.jpg'
    author:
        - Suzanne Collins
    published: 2025-03-18
    tags:
        - young-adult
        - dystopian
        - science-fiction
        - fiction
    rating: 3.5
    pages: 400
    lists:
        - 2025 Reads
        - Hunger Games
    comment: Good, but not as riveting as the original series

    """
    # Parse the content
    try:
        with open(book_file, "r") as file:
            yaml_content = yaml.load(file, Loader=yaml.FullLoader)
    except yaml.YAMLError as e:
        print(f"Error parsing book file {book_file}: {e}")
        return None

    # Validate the minimum required fields are present
    if not all(field in yaml_content for field in ["title", "author", "published"]):
        print(f"Error: Missing required fields in book file {book_file}")
        return None

    book = Book(
        title=yaml_content["title"],
        author=yaml_content["author"],
        published=yaml_content["published"],
        directory=directory,
    )
    # Add the remaining properties to the book
    for key, value in yaml_content.items():
        if key not in ["title", "author", "published"]:
            book.add_property(key, value)

    return book
