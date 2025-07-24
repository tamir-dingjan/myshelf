import yaml, datetime

class Book:
    def __init__(self, title: str, author: str, published: datetime.date):
        self.title = title
        self.author = author
        self.published = published
        self.properties = {}

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


def load_book_file(book_file: str):
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
        with open(book_file, 'r') as file:
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
    )
    # Add the remaining properties to the book
    for key, value in yaml_content.items():
        if key not in ["title", "author", "published"]:
            book.add_property(key, value)

    return book

