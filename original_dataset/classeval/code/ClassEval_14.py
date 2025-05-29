import sqlite3

class BookManagementDB:

    def __init__(self, db_name):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('\n            CREATE TABLE IF NOT EXISTS books (\n                id INTEGER PRIMARY KEY,\n                title TEXT,\n                author TEXT,\n                available INTEGER\n            )\n        ')
        self.connection.commit()

    def add_book(self, title, author):
        self.cursor.execute('\n            INSERT INTO books (title, author, available)\n            VALUES (?, ?, 1)\n        ', (title, author))
        self.connection.commit()

    def remove_book(self, book_id):
        self.cursor.execute('\n            DELETE FROM books WHERE id = ?\n        ', (book_id,))
        self.connection.commit()

    def borrow_book(self, book_id):
        self.cursor.execute('\n            UPDATE books SET available = 0 WHERE id = ?\n        ', (book_id,))
        self.connection.commit()

    def return_book(self, book_id):
        self.cursor.execute('\n            UPDATE books SET available = 1 WHERE id = ?\n        ', (book_id,))
        self.connection.commit()

    def search_books(self):
        self.cursor.execute('\n            SELECT * FROM books\n        ')
        books = self.cursor.fetchall()
        return books