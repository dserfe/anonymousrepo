import sqlite3

class StudentDatabaseProcessor:

    def __init__(self, database_name):
        self.database_name = database_name

    def create_student_table(self):
        conn = sqlite3.connect(self.database_name)
        cursor = conn.cursor()
        create_table_query = '\n        CREATE TABLE IF NOT EXISTS students (\n            id INTEGER PRIMARY KEY,\n            name TEXT,\n            age INTEGER,\n            gender TEXT,\n            grade INTEGER\n        )\n        '
        cursor.execute(create_table_query)
        conn.commit()
        conn.close()

    def insert_student(self, student_data):
        conn = sqlite3.connect(self.database_name)
        cursor = conn.cursor()
        insert_query = '\n        INSERT INTO students (name, age, gender, grade)\n        VALUES (?, ?, ?, ?)\n        '
        cursor.execute(insert_query, (student_data['name'], student_data['age'], student_data['gender'], student_data['grade']))
        conn.commit()
        conn.close()

    def search_student_by_name(self, name):
        conn = sqlite3.connect(self.database_name)
        cursor = conn.cursor()
        select_query = 'SELECT * FROM students WHERE name = ?'
        cursor.execute(select_query, (name,))
        result = cursor.fetchall()
        conn.close()
        return result

    def delete_student_by_name(self, name):
        conn = sqlite3.connect(self.database_name)
        cursor = conn.cursor()
        delete_query = 'DELETE FROM students WHERE name = ?'
        cursor.execute(delete_query, (name,))
        conn.commit()
        conn.close()