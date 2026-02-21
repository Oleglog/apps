from typing import List, Dict

class Book:
    def __init__(self, title: str, author: str):
        self.title = title
        self.author = author
        self.borrowed_by = None  # Читатель, который взял книгу

    def __repr__(self):
        return f"<Book: {self.title} by {self.author}>"

class Reader:
    def __init__(self, name: str):
        self.name = name
        self.borrowed_books: List[Book] = []

    def __repr__(self):
        return f"<Reader: {self.name}>"

class Library:
    def __init__(self):
        self.books: List[Book] = []
        self.readers: List[Reader] = []

    # --- Книги ---
    def add_book(self, book: Book):
        self.books.append(book)

    def remove_book(self, book: Book):
        if book in self.books:
            if book.borrowed_by:
                raise ValueError(f"Book '{book.title}' is currently borrowed!")
            self.books.remove(book)

    # --- Читатели ---
    def register_reader(self, reader: Reader):
        self.readers.append(reader)

    # --- Выдача и возврат ---
    def borrow_book(self, book: Book, reader: Reader):
        if book.borrowed_by:
            raise ValueError(f"Book '{book.title}' is already borrowed by {book.borrowed_by.name}")
        book.borrowed_by = reader
        reader.borrowed_books.append(book)

    def return_book(self, book: Book, reader: Reader):
        if book.borrowed_by != reader:
            raise ValueError(f"Book '{book.title}' was not borrowed by {reader.name}")
        book.borrowed_by = None
        reader.borrowed_books.remove(book)

    def list_available_books(self):
        return [book for book in self.books if not book.borrowed_by]