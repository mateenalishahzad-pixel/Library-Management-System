"""
Advanced Search Algorithms for Library Management System
Implements multiple search strategies for performance comparison
"""

from typing import List, Dict, Set, Optional
from dataclasses import dataclass
import sys
import os

# Add project root to path for imports
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

from src.models.book import Book


class TrieNode:
    """Trie node for prefix-based search"""
    
    def __init__(self):
        self.children: Dict[str, 'TrieNode'] = {}
        self.books: List[Book] = []
        self.is_end_of_word = False


class TrieSearch:
    """Trie-based search algorithm for efficient prefix matching"""
    
    def __init__(self):
        self.title_trie = TrieNode()
        self.author_trie = TrieNode()
        self.isbn_index: Dict[str, Book] = {}
    
    def build_index(self, books: List[Book]):
        """Build trie indexes for books"""
        self.title_trie = TrieNode()
        self.author_trie = TrieNode()
        self.isbn_index = {}
        
        for book in books:
            # Index by title
            self._insert_into_trie(self.title_trie, book.title.lower(), book)
            
            # Index by author
            self._insert_into_trie(self.author_trie, book.author.lower(), book)
            
            # Index by ISBN
            self.isbn_index[book.isbn] = book
    
    def _insert_into_trie(self, root: TrieNode, text: str, book: Book):
        """Insert a book into the trie"""
        node = root
        for char in text:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
            node.books.append(book)
        node.is_end_of_word = True
    
    def search(self, query: str) -> List[Book]:
        """Search for books using trie"""
        query_lower = query.lower()
        results = set()
        
        # Search in title trie
        title_results = self._search_in_trie(self.title_trie, query_lower)
        results.update(title_results)
        
        # Search in author trie
        author_results = self._search_in_trie(self.author_trie, query_lower)
        results.update(author_results)
        
        # Search in ISBN index
        if query in self.isbn_index:
            results.add(self.isbn_index[query])
        
        return list(results)
    
    def _search_in_trie(self, root: TrieNode, query: str) -> List[Book]:
        """Search for prefix matches in trie"""
        node = root
        for char in query:
            if char not in node.children:
                return []
            node = node.children[char]
        return node.books


class InvertedIndexSearch:
    """Inverted index search for efficient text retrieval"""
    
    def __init__(self):
        self.word_index: Dict[str, Set[Book]] = {}
        self.isbn_index: Dict[str, Book] = {}
    
    def build_index(self, books: List[Book]):
        """Build inverted index from books"""
        self.word_index = {}
        self.isbn_index = {}
        
        for book in books:
            # Index ISBN
            self.isbn_index[book.isbn] = book
            
            # Tokenize and index title words
            title_words = self._tokenize(book.title)
            for word in title_words:
                if word not in self.word_index:
                    self.word_index[word] = set()
                self.word_index[word].add(book)
            
            # Tokenize and index author words
            author_words = self._tokenize(book.author)
            for word in author_words:
                if word not in self.word_index:
                    self.word_index[word] = set()
                self.word_index[word].add(book)
    
    def _tokenize(self, text: str) -> List[str]:
        """Tokenize text into words"""
        # Simple tokenization - split on whitespace and punctuation
        import re
        words = re.findall(r'\b\w+\b', text.lower())
        return words
    
    def search(self, query: str) -> List[Book]:
        """Search using inverted index"""
        query_words = self._tokenize(query)
        results = set()
        
        # Check ISBN first
        if query in self.isbn_index:
            results.add(self.isbn_index[query])
        
        # Search for each word in query
        for word in query_words:
            if word in self.word_index:
                if not results:
                    results = self.word_index[word].copy()
                else:
                    # Intersection for multi-word queries
                    results = results.intersection(self.word_index[word])
        
        return list(results)


class BinarySearchLibrary:
    """Binary search implementation for sorted book collections"""
    
    def __init__(self):
        self.books_by_title: List[Book] = []
        self.books_by_author: List[Book] = []
        self.isbn_index: Dict[str, Book] = {}
    
    def build_index(self, books: List[Book]):
        """Build sorted indexes for binary search"""
        # Sort books by title and author
        self.books_by_title = sorted(books, key=lambda b: b.title.lower())
        self.books_by_author = sorted(books, key=lambda b: b.author.lower())
        
        # Build ISBN index for O(1) lookup
        self.isbn_index = {book.isbn: book for book in books}
    
    def search_by_title(self, query: str) -> List[Book]:
        """Binary search by title"""
        query_lower = query.lower()
        left, right = 0, len(self.books_by_title) - 1
        results = []
        
        # Find first occurrence
        while left <= right:
            mid = (left + right) // 2
            title = self.books_by_title[mid].title.lower()
            
            if query_lower in title:
                # Found a match, expand to find all matches
                results.append(self.books_by_title[mid])
                
                # Search left for more matches
                i = mid - 1
                while i >= 0 and query_lower in self.books_by_title[i].title.lower():
                    results.append(self.books_by_title[i])
                    i -= 1
                
                # Search right for more matches
                i = mid + 1
                while i < len(self.books_by_title) and query_lower in self.books_by_title[i].title.lower():
                    results.append(self.books_by_title[i])
                    i += 1
                
                break
            elif query_lower < title:
                right = mid - 1
            else:
                left = mid + 1
        
        return results
    
    def search_by_author(self, query: str) -> List[Book]:
        """Binary search by author"""
        query_lower = query.lower()
        left, right = 0, len(self.books_by_author) - 1
        results = []
        
        while left <= right:
            mid = (left + right) // 2
            author = self.books_by_author[mid].author.lower()
            
            if query_lower in author:
                results.append(self.books_by_author[mid])
                
                # Search for more matches
                i = mid - 1
                while i >= 0 and query_lower in self.books_by_author[i].author.lower():
                    results.append(self.books_by_author[i])
                    i -= 1
                
                i = mid + 1
                while i < len(self.books_by_author) and query_lower in self.books_by_author[i].author.lower():
                    results.append(self.books_by_author[i])
                    i += 1
                
                break
            elif query_lower < author:
                right = mid - 1
            else:
                left = mid + 1
        
        return results
    
    def search(self, query: str) -> List[Book]:
        """Combined search using binary search"""
        results = set()
        
        # Check ISBN first
        if query in self.isbn_index:
            results.add(self.isbn_index[query])
        
        # Search by title and author
        results.update(self.search_by_title(query))
        results.update(self.search_by_author(query))
        
        return list(results)


class HybridSearch:
    """Hybrid search combining multiple algorithms"""
    
    def __init__(self):
        self.trie_search = TrieSearch()
        self.inverted_search = InvertedIndexSearch()
        self.binary_search = BinarySearchLibrary()
    
    def build_index(self, books: List[Book]):
        """Build all search indexes"""
        self.trie_search.build_index(books)
        self.inverted_search.build_index(books)
        self.binary_search.build_index(books)
    
    def search(self, query: str, algorithm: str = "hybrid") -> List[Book]:
        """Search using specified algorithm"""
        if algorithm == "trie":
            return self.trie_search.search(query)
        elif algorithm == "inverted":
            return self.inverted_search.search(query)
        elif algorithm == "binary":
            return self.binary_search.search(query)
        elif algorithm == "hybrid":
            # Combine results from all algorithms
            results = set()
            results.update(self.trie_search.search(query))
            results.update(self.inverted_search.search(query))
            results.update(self.binary_search.search(query))
            return list(results)
        else:
            raise ValueError(f"Unknown algorithm: {algorithm}")


def test_search_algorithms():
    """Test function to demonstrate search algorithms"""
    from ..performance.benchmark import PerformanceBenchmark
    
    # Generate test data
    benchmark = PerformanceBenchmark()
    books = benchmark.generate_test_books(1000)
    
    # Test different search algorithms
    hybrid = HybridSearch()
    hybrid.build_index(books)
    
    # Test queries
    queries = ["programming", "smith", "algorithms", "johnson"]
    
    print("Testing Advanced Search Algorithms")
    print("=" * 50)
    
    for query in queries:
        print(f"\nQuery: '{query}'")
        
        # Test each algorithm
        trie_results = hybrid.search(query, "trie")
        inverted_results = hybrid.search(query, "inverted")
        binary_results = hybrid.search(query, "binary")
        hybrid_results = hybrid.search(query, "hybrid")
        
        print(f"Trie Search: {len(trie_results)} results")
        print(f"Inverted Index: {len(inverted_results)} results")
        print(f"Binary Search: {len(binary_results)} results")
        print(f"Hybrid Search: {len(hybrid_results)} results")


if __name__ == "__main__":
    test_search_algorithms()
