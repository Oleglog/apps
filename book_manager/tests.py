import unittest
from main import Book, Reader, Library

class TestLibrary(unittest.TestCase):

    def setUp(self):
        self.library = Library()
        self.book1 = Book("1984", "George Orwell")
        self.book2 = Book("Brave New World", "Aldous Huxley")
        self.reader = Reader("Alice")

    def test_add_remove_book(self):
        self.library.add_book(self.book1)
        self.assertIn(self.book1, self.library.books)
        self.library.remove_book(self.book1)
        self.assertNotIn(self.book1, self.library.books)

    def test_remove_borrowed_book(self):
        self.library.add_book(self.book1)
        self.library.register_reader(self.reader)
        self.library.borrow_book(self.book1, self.reader)
        with self.assertRaises(ValueError):
            self.library.remove_book(self.book1)

    def test_borrow_and_return_book(self):
        self.library.add_book(self.book1)
        self.library.register_reader(self.reader)
        self.library.borrow_book(self.book1, self.reader)
        self.assertEqual(self.book1.borrowed_by, self.reader)
        self.assertIn(self.book1, self.reader.borrowed_books)

        self.library.return_book(self.book1, self.reader)
        self.assertIsNone(self.book1.borrowed_by)
        self.assertNotIn(self.book1, self.reader.borrowed_books)

    def test_borrow_already_borrowed_book(self):
        self.library.add_book(self.book1)
        reader2 = Reader("Bob")
        self.library.register_reader(self.reader)
        self.library.register_reader(reader2)
        self.library.borrow_book(self.book1, self.reader)
        with self.assertRaises(ValueError):
            self.library.borrow_book(self.book1, reader2)

    def test_return_not_borrowed_book(self):
        self.library.add_book(self.book1)
        self.library.register_reader(self.reader)
        with self.assertRaises(ValueError):
            self.library.return_book(self.book1, self.reader)

if __name__ == "__main__":
    unittest.main()