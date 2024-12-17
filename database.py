import sqlite3
import logging

logging.basicConfig(filename = 'app.log', level = logging.ERROR,
                    format = '%(asctime)s %(levelname)s %(message)s')

class Database:
    def __init__(self, db_path):
        self.db_path = db_path
        self.init_db()

    def init_db(self):
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS users (
                               id INTERGER PRIMARY KEY AUTOINCREMENT,
                                question TEXT NOT NULL,
                               answer TEXT NOT NULL,
                               options TEXT NOT NULL
                               )
                ''')
                conn.commit()
        except sqlite3.Error as e:
            logging.error(f'Database error: {e}')

    def fetch_questions():
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM questions")
                return cursor.fetchall()
        except sqlite3.Error as e:
            logging.error(f'Database error: {e}')
            return []
        
    def add_questions(self, question, answer, options):
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO questions (question, answer, options) VALUES (?, ?, ?)", (question, answer, options))
                conn.commit()
        except sqlite3.Error as e:
            logging.error(f'Database error saat menambahkan pertanyaan: {e}')

    def update_question(self, question_id, question, answer, options):
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                               UPDATE questions
                               SET question = ?, answer = ?, options = ?
                               WHERE id = ?)
                            """, (question, answer, options, question_id))
                conn.commit()
        except sqlite3.Error as e:
            logging.error(f'Database error saat memperbarui pertanyaan: {e}')
    
    def delete_question(self, question_id):
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM questions WHERE id = ?", (question_id,))
                conn.commit()
        except sqlite3.Error as e:
            logging.error(f'Database error saat menghapus pertanyaan: {e}')

