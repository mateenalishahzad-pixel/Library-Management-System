"""
Performance Benchmark Suite for Library Management System
Compares different algorithms for search, sorting, and data structures
"""

import time
import random
import string
from typing import List, Dict, Any
from dataclasses import dataclass
import sys
import os

# Add project root to path for imports
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

from src.models.book import Book
from src.services.library import Library


@dataclass
class BenchmarkResult:
    """Stores benchmark results for algorithm comparison"""
    algorithm_name: str
    operation: str
    data_size: int
    execution_time: float
    memory_usage: int = 0
    additional_metrics: Dict[str, Any] = None


class PerformanceBenchmark:
    """Comprehensive performance testing framework"""
    
    def __init__(self):
        self.results: List[BenchmarkResult] = []
        self.test_data_sizes = [100, 500, 1000, 5000, 10000]
    
    def generate_test_books(self, count: int) -> List[Book]:
        """Generate realistic test book data"""
        books = []
        authors = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis"]
        titles = ["Programming", "Algorithms", "Data Structures", "Software Engineering", 
                 "Database Systems", "Computer Networks", "Artificial Intelligence", 
                 "Machine Learning", "Web Development", "Mobile Computing"]
        
        for i in range(count):
            isbn = f"ISBN-{random.randint(1000000000, 9999999999)}"
            title = f"{random.choice(titles)} {i}"
            author = f"{random.choice(authors)} {random.randint(1, 100)}"
            year = random.randint(1990, 2024)
            books.append(Book(isbn=isbn, title=title, author=author, publication_year=year))
        
        return books
    
    def benchmark_linear_search(self, books: List[Book], queries: List[str]) -> float:
        """Benchmark current linear search implementation"""
        start_time = time.time()
        
        for query in queries:
            # Current linear search implementation
            results = []
            query_lower = query.lower()
            for book in books:
                if (query_lower in book.title.lower() or 
                    query_lower in book.author.lower() or 
                    query_lower in book.isbn):
                    results.append(book)
        
        end_time = time.time()
        return end_time - start_time
    
    def benchmark_binary_search(self, books: List[Book], queries: List[str]) -> float:
        """Benchmark binary search on sorted books"""
        # Sort books by title for binary search
        sorted_books = sorted(books, key=lambda b: b.title.lower())
        titles = [book.title.lower() for book in sorted_books]
        
        start_time = time.time()
        
        for query in queries:
            query_lower = query.lower()
            # Binary search implementation
            left, right = 0, len(titles) - 1
            results = []
            
            while left <= right:
                mid = (left + right) // 2
                if query_lower in titles[mid]:
                    # Found match, expand to find all matches
                    results.append(sorted_books[mid])
                    # Check surrounding elements for additional matches
                    i = mid - 1
                    while i >= 0 and query_lower in titles[i]:
                        results.append(sorted_books[i])
                        i -= 1
                    i = mid + 1
                    while i < len(titles) and query_lower in titles[i]:
                        results.append(sorted_books[i])
                        i += 1
                    break
                elif query_lower < titles[mid]:
                    right = mid - 1
                else:
                    left = mid + 1
        
        end_time = time.time()
        return end_time - start_time
    
    def benchmark_hash_search(self, books: List[Book], queries: List[str]) -> float:
        """Benchmark hash-based search"""
        # Create hash maps for different search fields
        title_map = {}
        author_map = {}
        isbn_map = {}
        
        for book in books:
            title_lower = book.title.lower()
            if title_lower not in title_map:
                title_map[title_lower] = []
            title_map[title_lower].append(book)
            
            author_lower = book.author.lower()
            if author_lower not in author_map:
                author_map[author_lower] = []
            author_map[author_lower].append(book)
            
            isbn_map[book.isbn] = book
        
        start_time = time.time()
        
        for query in queries:
            query_lower = query.lower()
            results = []
            
            # Check title hash map
            if query_lower in title_map:
                results.extend(title_map[query_lower])
            
            # Check author hash map
            if query_lower in author_map:
                results.extend(author_map[query_lower])
            
            # Check ISBN hash map
            if query in isbn_map:
                results.append(isbn_map[query])
        
        end_time = time.time()
        return end_time - start_time
    
    def benchmark_sorting_algorithms(self, books: List[Book]) -> Dict[str, float]:
        """Benchmark different sorting algorithms"""
        results = {}
        
        # QuickSort implementation
        def quicksort(arr):
            if len(arr) <= 1:
                return arr
            pivot = arr[len(arr) // 2]
            left = [x for x in arr if x.title.lower() < pivot.title.lower()]
            middle = [x for x in arr if x.title.lower() == pivot.title.lower()]
            right = [x for x in arr if x.title.lower() > pivot.title.lower()]
            return quicksort(left) + middle + quicksort(right)
        
        # MergeSort implementation
        def mergesort(arr):
            if len(arr) <= 1:
                return arr
            mid = len(arr) // 2
            left = mergesort(arr[:mid])
            right = mergesort(arr[mid:])
            return self._merge(left, right)
        
        # Benchmark QuickSort
        start_time = time.time()
        quicksort(books.copy())
        results["quicksort"] = time.time() - start_time
        
        # Benchmark MergeSort
        start_time = time.time()
        mergesort(books.copy())
        results["mergesort"] = time.time() - start_time
        
        # Benchmark Python's built-in sort (TimSort)
        start_time = time.time()
        sorted(books, key=lambda b: b.title.lower())
        results["timsort"] = time.time() - start_time
        
        return results
    
    def _merge(self, left: List[Book], right: List[Book]) -> List[Book]:
        """Helper function for merge sort"""
        result = []
        i = j = 0
        
        while i < len(left) and j < len(right):
            if left[i].title.lower() <= right[j].title.lower():
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        
        result.extend(left[i:])
        result.extend(right[j:])
        return result
    
    def run_search_benchmarks(self):
        """Run comprehensive search algorithm benchmarks"""
        print("Running Search Algorithm Benchmarks...")
        
        for size in self.test_data_sizes:
            print(f"Testing with {size} books...")
            books = self.generate_test_books(size)
            queries = ["programming", "smith", "ISBN-1234567890", "algorithms", "johnson"]
            
            # Benchmark Linear Search
            linear_time = self.benchmark_linear_search(books, queries)
            self.results.append(BenchmarkResult(
                "Linear Search", "search", size, linear_time
            ))
            
            # Benchmark Binary Search
            binary_time = self.benchmark_binary_search(books, queries)
            self.results.append(BenchmarkResult(
                "Binary Search", "search", size, binary_time
            ))
            
            # Benchmark Hash Search
            hash_time = self.benchmark_hash_search(books, queries)
            self.results.append(BenchmarkResult(
                "Hash Search", "search", size, hash_time
            ))
    
    def run_sorting_benchmarks(self):
        """Run sorting algorithm benchmarks"""
        print("Running Sorting Algorithm Benchmarks...")
        
        for size in self.test_data_sizes:
            print(f"Testing with {size} books...")
            books = self.generate_test_books(size)
            
            sort_results = self.benchmark_sorting_algorithms(books)
            
            for algorithm, time_taken in sort_results.items():
                self.results.append(BenchmarkResult(
                    algorithm.capitalize(), "sort", size, time_taken
                ))
    
    def run_data_structure_benchmarks(self):
        """Benchmark different data structure operations"""
        print("Running Data Structure Benchmarks...")
        
        for size in self.test_data_sizes:
            print(f"Testing with {size} books...")
            books = self.generate_test_books(size)
            
            # Benchmark Dictionary (current implementation)
            start_time = time.time()
            book_dict = {}
            for book in books:
                book_dict[book.isbn] = book
            dict_insert_time = time.time() - start_time
            
            # Benchmark Dictionary lookup
            start_time = time.time()
            for book in books[:100]:  # Test first 100 lookups
                _ = book_dict.get(book.isbn)
            dict_lookup_time = time.time() - start_time
            
            self.results.append(BenchmarkResult(
                "Dictionary Insert", "insert", size, dict_insert_time
            ))
            self.results.append(BenchmarkResult(
                "Dictionary Lookup", "lookup", size, dict_lookup_time
            ))
    
    def generate_report(self) -> str:
        """Generate comprehensive performance report"""
        report = []
        report.append("=" * 80)
        report.append("LIBRARY MANAGEMENT SYSTEM - PERFORMANCE ANALYSIS REPORT")
        report.append("=" * 80)
        report.append("")
        
        # Group results by operation
        search_results = [r for r in self.results if r.operation == "search"]
        sort_results = [r for r in self.results if r.operation == "sort"]
        data_results = [r for r in self.results if r.operation in ["insert", "lookup"]]
        
        # Search Algorithm Comparison
        report.append("SEARCH ALGORITHM PERFORMANCE")
        report.append("-" * 40)
        report.append(f"{'Algorithm':<15} {'Data Size':<10} {'Time (s)':<12} {'Complexity':<12}")
        report.append("-" * 65)
        
        for size in self.test_data_sizes:
            size_search = [r for r in search_results if r.data_size == size]
            for result in size_search:
                complexity = self._get_complexity(result.algorithm_name)
                report.append(f"{result.algorithm_name:<15} {result.data_size:<10} {result.execution_time:<12.6f} {complexity:<12}")
            report.append("")
        
        # Sorting Algorithm Comparison
        report.append("SORTING ALGORITHM PERFORMANCE")
        report.append("-" * 40)
        report.append(f"{'Algorithm':<15} {'Data Size':<10} {'Time (s)':<12} {'Complexity':<12}")
        report.append("-" * 65)
        
        for size in self.test_data_sizes:
            size_sort = [r for r in sort_results if r.data_size == size]
            for result in size_sort:
                complexity = self._get_complexity(result.algorithm_name)
                report.append(f"{result.algorithm_name:<15} {result.data_size:<10} {result.execution_time:<12.6f} {complexity:<12}")
            report.append("")
        
        # Data Structure Performance
        report.append("DATA STRUCTURE PERFORMANCE")
        report.append("-" * 40)
        report.append(f"{'Operation':<15} {'Data Size':<10} {'Time (s)':<12} {'Complexity':<12}")
        report.append("-" * 65)
        
        for size in self.test_data_sizes:
            size_data = [r for r in data_results if r.data_size == size]
            for result in size_data:
                complexity = self._get_complexity(result.algorithm_name)
                report.append(f"{result.algorithm_name:<15} {result.data_size:<10} {result.execution_time:<12.6f} {complexity:<12}")
            report.append("")
        
        # Performance Analysis Summary
        report.append("PERFORMANCE ANALYSIS SUMMARY")
        report.append("-" * 40)
        
        # Find best performing algorithms
        best_search = min(search_results, key=lambda x: x.execution_time)
        best_sort = min(sort_results, key=lambda x: x.execution_time)
        
        report.append(f"Best Search Algorithm: {best_search.algorithm_name}")
        report.append(f"Best Sorting Algorithm: {best_sort.algorithm_name}")
        report.append("")
        
        # Recommendations
        report.append("RECOMMENDATIONS")
        report.append("-" * 40)
        report.append("1. For large datasets (>1000 books), Hash Search provides O(1) average performance")
        report.append("2. Python's built-in TimSort is optimal for sorting operations")
        report.append("3. Dictionary operations provide excellent performance for book management")
        report.append("4. Consider implementing caching for frequently searched books")
        report.append("5. For very large libraries, consider database indexing")
        
        return "\n".join(report)
    
    def _get_complexity(self, algorithm_name: str) -> str:
        """Get time complexity for algorithm"""
        complexity_map = {
            "Linear Search": "O(n)",
            "Binary Search": "O(log n)",
            "Hash Search": "O(1)",
            "Quicksort": "O(n log n)",
            "Mergesort": "O(n log n)",
            "Timsort": "O(n log n)",
            "Dictionary Insert": "O(1)",
            "Dictionary Lookup": "O(1)"
        }
        return complexity_map.get(algorithm_name, "Unknown")
    
    def save_report(self, filename: str = "performance_report.txt"):
        """Save performance report to file"""
        report = self.generate_report()
        with open(filename, 'w') as f:
            f.write(report)
        print(f"Performance report saved to {filename}")


def main():
    """Main function to run all benchmarks"""
    benchmark = PerformanceBenchmark()
    
    print("Starting Library Management System Performance Analysis...")
    print("=" * 60)
    
    # Run all benchmarks
    benchmark.run_search_benchmarks()
    benchmark.run_sorting_benchmarks()
    benchmark.run_data_structure_benchmarks()
    
    # Generate and save report
    print("\nGenerating performance report...")
    benchmark.save_report()
    
    # Display summary
    print("\n" + benchmark.generate_report())


if __name__ == "__main__":
    main()
