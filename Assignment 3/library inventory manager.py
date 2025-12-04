# Name: Bhoomi Raghav
# Roll number: 2501730254
# Course Code: ETCCPP102
# Assignment: Library Inventory Manager (OOP)
# Date: 2025-12-08

import json
from pathlib import Path
import logging

# --- Configuration ---
CATALOG_FILE = Path("library_catalog.json")
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Task 1: Book Class Design ---

class Book:
    """Represents a single book in the library inventory."""
    def __init__(self, title, author, isbn, status='available'):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.status = status # 'available' or 'issued'

    def __str__(self):
        """Magic method for user-friendly printing."""
        return f"Title: {self.title:<30} | Author: {self.author:<20} | ISBN: {self.isbn:<13} | Status: {self.status.capitalize()}"

    def to_dict(self):
        """Converts the Book object to a dictionary for JSON serialization."""
        return {
            'title': self.title,
            'author': self.author,
            'isbn': self.isbn,
            'status': self.status
        }
        
    @classmethod
    def from_dict(cls, data):
        """Creates a Book object from a dictionary."""
        return cls(data['title'], data['author'], data['isbn'], data['status'])

    def issue(self):
        """Changes the book status to 'issued' if available."""
        if self.is_available():
            self.status = 'issued'
            logging.info(f"Book issued: {self.title}")
            return True
        else:
            print(f"Error: '{self.title}' is already issued.")
            return False

    def return_book(self):
        """Changes the book status back to 'available' if issued."""
        if self.status == 'issued':
            self.status = 'available'
            logging.info(f"Book returned: {self.title}")
            return True
        else:
            print(f"Error: '{self.title}' was not issued.")
            return False

    def is_available(self):
        """Checks if the book is available."""
        return self.status == 'available'

# --- Task 2: Inventory Manager & Task 3: File Persistence ---

class LibraryManager:
    """Manages the collection of Book objects and handles persistence."""
    def __init__(self, filepath=CATALOG_FILE):
        self.filepath = filepath
        self.books = []
        self._load_catalog()

    def _load_catalog(self):
        """Load book catalog from JSON file. Robust File Handling."""
        try:
            if self.filepath.exists():
                with self.filepath.open(mode='r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.books = [Book.from_dict(item) for item in data]
                logging.info(f"Successfully loaded {len(self.books)} books from {self.filepath}")
            else:
                logging.warning(f"Catalog file not found at {self.filepath}. Starting with empty inventory.")
        except json.JSONDecodeError:
            print(f"Error: Catalog file '{self.filepath}' is corrupted. Starting with empty inventory.")
            self.books = []
        except Exception as e:
            print(f"An unexpected error occurred during loading: {e}")
            self.books = []
        finally:
            # Ensures books is initialized even if loading fails
            logging.debug("Catalog loading process finished.")


    def _save_catalog(self):
        """Save the current book catalog to the JSON file."""
        data = [book.to_dict() for book in self.books]
        try:
            with self.filepath.open(mode='w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)
            logging.info(f"Catalog saved with {len(self.books)} books.")
        except IOError as e:
            logging.error(f"Error saving catalog to file: {e}")
            print("Error: Could not save the inventory to file.")

    def add_book(self, title, author, isbn):
        """Adds a new book to the inventory and saves the catalog."""
        if any(book.isbn == isbn for book in self.books):
            print(f"Error: Book with ISBN {isbn} already exists.")
            return
        
        new_book = Book(title.title(), author.title(), isbn)
        self.books.append(new_book)
        self._save_catalog()
        print(f"Success: Book '{title}' added to inventory.")

    def search_by_title(self, query):
        """Searches for books whose title contains the query string (case-insensitive)."""
        query = query.lower()
        results = [book for book in self.books if query in book.title.lower()]
        return results

    def search_by_isbn(self, isbn):
        """Searches for a book by its exact ISBN."""
        return next((book for book in self.books if book.isbn == isbn), None)

    def display_all(self):
        """Displays all books in the inventory."""
        if not self.books:
            print("\nThe library inventory is currently empty.")
            return
        
        print("\n" + "="*80)
        print(f"{'TITLE':<35}{'AUTHOR':<25}{'ISBN':<15}{'STATUS':<15}")
        print("="*80)
        for book in self.books:
            status_color = "\033[92m" if book.is_available() else "\033[91m" # Green/Red color for status
            reset_color = "\033[0m"
            print(f"{book.title:<35.34}{book.author:<25.24}{book.isbn:<15.14}{status_color}{book.status.capitalize():<15}{reset_color}")
        print("="*80)

    def issue_return_book(self, isbn, action):
        """Helper for issuing or returning a book."""
        book = self.search_by_isbn(isbn)
        if not book:
            print(f"Error: No book found with ISBN {isbn}.")
            return False

        success = False
        if action == 'issue':
            success = book.issue()
        elif action == 'return':
            success = book.return_book()
        
        if success:
            self._save_catalog()
        return success

# --- Task 4: Menu-Driven Command Line Interface ---

def run_cli():
    """Main menu loop for the Library Inventory Manager."""
    manager = LibraryManager()

    while True:
        print("\n" + "="*40)
        print("  Library Inventory Manager (ETCCPP102) ")
        print("="*40)
        print("1. Add New Book")
        print("2. Issue Book")
        print("3. Return Book")
        print("4. View All Books")
        print("5. Search by Title")
        print("6. Exit")
        print("-" * 40)
        
        choice = input("Enter choice (1-6): ").strip()
        
        try:
            if choice == '1':
                title = input("Enter Title: ").strip()
                author = input("Enter Author: ").strip()
                isbn = input("Enter ISBN (unique 10-13 digits): ").strip()
                if title and author and isbn.isdigit():
                    manager.add_book(title, author, isbn)
                else:
                    print("Error: All fields are required, and ISBN must be numeric.")
            
            elif choice == '2':
                isbn = input("Enter ISBN of the book to issue: ").strip()
                manager.issue_return_book(isbn, 'issue')
            
            elif choice == '3':
                isbn = input("Enter ISBN of the book to return: ").strip()
                manager.issue_return_book(isbn, 'return')
                
            elif choice == '4':
                manager.display_all()

            elif choice == '5':
                query = input("Enter title keyword to search: ").strip()
                results = manager.search_by_title(query)
                if results:
                    print(f"\nFound {len(results)} books matching '{query}':")
                    for book in results:
                        print(f"  - {book}")
                else:
                    print(f"No books found matching '{query}'.")

            elif choice == '6':
                print("Exiting Library Manager. Catalog data saved.")
                break
                
            else:
                print("Invalid choice. Please enter a number from 1 to 6.")
                
        except Exception as e:
            # Task 5: General exception handling
            logging.exception("An unhandled error occurred in the CLI loop.")
            print(f"\nSystem Error: {e}. Please check the log for details.")

if __name__ == "__main__":
    run_cli()