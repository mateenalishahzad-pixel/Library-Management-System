from dataclasses import dataclass, field
from typing import List


@dataclass
class User:
    user_id: str
    name: str
    borrowed_books: List[str] = field(default_factory=list)

    def __str__(self):
        return f"{self.name} (ID: {self.user_id})"
