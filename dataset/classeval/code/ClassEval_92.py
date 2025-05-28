import sqlite3

class UserLoginDB:

    def __init__(self, db_name):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()

    def insert_user(self, username, password):
        self.cursor.execute('\n            INSERT INTO users (username, password)\n            VALUES (?, ?)\n        ', (username, password))
        self.connection.commit()

    def search_user_by_username(self, username):
        self.cursor.execute('\n            SELECT * FROM users WHERE username = ?\n        ', (username,))
        user = self.cursor.fetchone()
        return user

    def delete_user_by_username(self, username):
        self.cursor.execute('\n            DELETE FROM users WHERE username = ?\n        ', (username,))
        self.connection.commit()

    def validate_user_login(self, username, password):
        user = self.search_user_by_username(username)
        if user is not None and user[1] == password:
            return True
        return False