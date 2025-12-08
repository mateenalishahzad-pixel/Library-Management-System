from dataclasses import dataclass


@dataclass
class Book:
    isbn: str
    title: str
    author: str
    publication_year: int
    available: bool = True

    def __str__(self):
        return f"{self.title} by {self.author} ({self.publication_year})"
