import sqlite3

class MovieTicketDB:

    def __init__(self, db_name):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('\n            CREATE TABLE IF NOT EXISTS tickets (\n                id INTEGER PRIMARY KEY,\n                movie_name TEXT,\n                theater_name TEXT,\n                seat_number TEXT,\n                customer_name TEXT\n            )\n        ')
        self.connection.commit()

    def insert_ticket(self, movie_name, theater_name, seat_number, customer_name):
        self.cursor.execute('\n            INSERT INTO tickets (movie_name, theater_name, seat_number, customer_name)\n            VALUES (?, ?, ?, ?)\n        ', (movie_name, theater_name, seat_number, customer_name))
        self.connection.commit()

    def search_tickets_by_customer(self, customer_name):
        self.cursor.execute('\n            SELECT * FROM tickets WHERE customer_name = ?\n        ', (customer_name,))
        tickets = self.cursor.fetchall()
        return tickets

    def delete_ticket(self, ticket_id):
        self.cursor.execute('\n            DELETE FROM tickets WHERE id = ?\n        ', (ticket_id,))
        self.connection.commit()