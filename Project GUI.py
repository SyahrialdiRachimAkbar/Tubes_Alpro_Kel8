import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import hashlib
import os
import logging
from database import Database

logging.basicConfig(filename = 'app.log', level = logging.ERROR,
                    format = '%(asctime)s %(levelname)s %(message)s')

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplikasi Kuis - Login/Registrasi")
        
        self.root.minsize(300, 200)

        # Inisialisasi Style
        self.style = ttk.Style()
        self.style.theme_use('clam')

        # Path ke subfolder dan file database
        self.DATA_FOLDER = 'database'
        self.DB_PATH = os.path.join(self.DATA_FOLDER, 'users.db')

        # Inisialisasi Database
        self.init_db()

        # Membuat UI utama
        self.create_main_ui()

    def init_db(self):
        if not os.path.exists(self.DATA_FOLDER):
            os.makedirs(self.DATA_FOLDER)

        with sqlite3.connect(self.DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL
                )
            ''')
            conn.commit()

    def create_main_ui(self):
        main_frame = ttk.Frame(self.root)
        main_frame.pack(expand=True, fill='both', padx=10, pady=10)

        label_title = ttk.Label(main_frame, text="Selamat Datang!", font=("Arial", 16))
        label_title.pack(pady=20)

        button_login = ttk.Button(main_frame, text="Login", width=15, command=self.open_login_window)
        button_login.pack(pady=10)

        button_register = ttk.Button(main_frame, text="Registrasi", width=15, command=self.open_register_window)
        button_register.pack(pady=10)

    def open_register_window(self):
        RegisterWindow(self)

    def open_login_window(self):
        LoginWindow(self)


class RegisterWindow:
    def __init__(self, app):
        self.app = app
        self.register_window = tk.Toplevel(app.root)
        self.register_window.title("Registrasi")
        self.register_window.minsize(350, 300)

        self.style = ttk.Style()
        self.style.theme_use('clam')

        reg_frame = ttk.Frame(self.register_window)
        reg_frame.pack(expand=True, fill='both', padx=10, pady=10)

        label_title = ttk.Label(reg_frame, text="Registrasi", font=("Arial", 16))
        label_title.pack(pady=10)

        frame_form = ttk.Frame(reg_frame)
        frame_form.pack(pady=10, fill='x')

        label_username = ttk.Label(frame_form, text="Username:")
        label_username.grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.entry_username = ttk.Entry(frame_form)
        self.entry_username.grid(row=0, column=1, padx=5, pady=5, sticky='w')

        label_password = ttk.Label(frame_form, text="Password:")
        label_password.grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.entry_password = ttk.Entry(frame_form, show="*")
        self.entry_password.grid(row=1, column=1, padx=5, pady=5, sticky='w')

        label_confirm_password = ttk.Label(frame_form, text="Konfirmasi Password:")
        label_confirm_password.grid(row=2, column=0, padx=5, pady=5, sticky='e')
        self.entry_confirm_password = ttk.Entry(frame_form, show="*")
        self.entry_confirm_password.grid(row=2, column=1, padx=5, pady=5, sticky='w')

        button_submit = ttk.Button(reg_frame, text="Daftar", command=self.submit_registration)
        button_submit.pack(pady=20)

    def submit_registration(self):
        username = self.entry_username.get().strip()
        password = self.entry_password.get().strip()
        confirm_password = self.entry_confirm_password.get().strip()

        # Validasi input
        if not username or not password or not confirm_password:
            messagebox.showerror("Error", "Semua field harus diisi.")
            return
        if len(username) < 4:
            messagebox.showerror("Error", "Username harus terdiri dari minimal 4 karakter.")
            return
        if len(password) < 6:
            messagebox.showerror("Error", "Password harus terdiri dari minimal 6 karakter.")
            return
        if password != confirm_password:
            messagebox.showerror("Error", "Password dan konfirmasi tidak cocok.")
            return
        if not username.isalnum():
            messagebox.showerror("Error", "Username hanya boleh mengandung huruf dan angka.")
            return

        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        try:
            with sqlite3.connect(self.app.DB_PATH) as conn:
                cursor = conn.cursor()
                cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
                conn.commit()
            messagebox.showinfo("Sukses", "Registrasi berhasil! Anda dapat login sekarang.")
            self.register_window.destroy()
        except sqlite3.IntegrityError as e:
            messagebox.showerror("Error", "Username sudah digunakan. Silakan pilih username lain.")
            logging.error(f"Username sudah ada di database: {e}")
        except sqlite3.OperationalError as e:
            messagebox.showerror("Error", "Gagal menyimpan data ke database.")
            logging.error(f"Database error: {e}")
        except sqlite3.Error as e:
            logging.error(f"Database error saat registrasi: {e}")
            messagebox.showerror("Error", f"Terjadi kesalahan pada database: {e}")
        else:
            messagebox.showinfo("Info", "Registrasi berhasil!")
            self.register_window.destroy()


class LoginWindow:
    def __init__(self, app):
        self.app = app
        self.login_window = tk.Toplevel(app.root)
        self.login_window.title("Login")
        self.login_window.minsize(350, 250)
        self.login_window.rowconfigure(0, weight=1)
        self.login_window.columnconfigure(0, weight=1)

        container = ttk.Frame(self.login_window)
        container.grid(row=0, column=0, sticky='nsew')
        

        container.rowconfigure(0, weight=1)
        container.columnconfigure(0, weight=1)

        frame_center = ttk.Frame(container)
        frame_center.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)


        frame_center.rowconfigure(1, weight=1) 
        frame_center.columnconfigure(0, weight=1)

        label_title = ttk.Label(frame_center, text="Login", font=("Arial", 16))
        label_title.grid(row=0, column=0, pady=10)

        frame_form = ttk.Frame(frame_center)
        frame_form.grid(row=1, column=0, sticky='nsew', pady=10)

        frame_form.columnconfigure(1, weight=1)

        label_username = ttk.Label(frame_form, text="Username:")
        label_username.grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.entry_username = ttk.Entry(frame_form)
        self.entry_username.grid(row=0, column=1, padx=5, pady=5, sticky='ew')

        label_password = ttk.Label(frame_form, text="Password:")
        label_password.grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.entry_password = ttk.Entry(frame_form, show="*")
        self.entry_password.grid(row=1, column=1, padx=5, pady=5, sticky='ew')

        button_login = ttk.Button(frame_center, text="Login", command=self.submit_login)    
        button_login.grid(row=2, column=0, pady=20)

    def submit_login(self):
        username = self.entry_username.get().strip()
        password = self.entry_password.get().strip()
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        try:
            with sqlite3.connect(self.app.DB_PATH) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT password FROM users WHERE username = ? ', (username,))
                stored_hashed_passwrod = cursor.fetchone()[0]
                

                if stored_hashed_passwrod == hashed_password:
                    messagebox.showinfo("Sukses", "Login berhasil!")
                    self.login_window.destroy()
                else:
                    messagebox.showerror("Error", "Username atau password salah.")
        except sqlite3.Error as e:
            logging.error(f"Database error saat login: {e}")
            messagebox.showerror("Error", f"Terjadi kesalahan pada database: {e}")        
        if username and password:
            messagebox.showinfo("Info", "Login dicoba!")
        else:
            messagebox.showerror("Error", "Semua field harus diisi.")




if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()



class ManageQuestionsWindow:
    def __init__(self, app):
        self.app = app
        self.window = tk.Toplevel(app.root)
        self.window.title("Kelola Soal")
        self.window.minsize(400, 400)

        # Tabel soal
        self.tree = ttk.Treeview(self.window, columns=("ID", "Soal", "Jawaban", "Opsi"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Soal", text="Soal")
        self.tree.heading("Jawaban", text="Jawaban")
        self.tree.heading("Opsi", text="Opsi")
        self.tree.pack(expand=True, fill='both', padx=10, pady=10)

        # Tombol CRUD
        button_frame = ttk.Frame(self.window)
        button_frame.pack(fill='x', padx=10, pady=10)

        ttk.Button(button_frame, text="Tambah Soal", command=self.add_question).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Edit Soal", command=self.edit_question).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Hapus Soal", command=self.delete_question).pack(side="left", padx=5)

        self.load_questions()

    def load_questions(self):
        """Memuat soal dari database dan menampilkan di tabel."""
        for row in self.tree.get_children():
            self.tree.delete(row)

        with sqlite3.connect(self.app.DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS questions (id INTEGER PRIMARY KEY, question TEXT, answer TEXT, options TEXT)")
            conn.commit()

            cursor.execute("SELECT * FROM questions")
            rows = cursor.fetchall()
            for row in rows:
                self.tree.insert('', 'end', values=row)

    def add_question(self):
        """Menambah soal baru."""
        AddQuestionWindow(self)

    def edit_question(self):
        """Mengedit soal yang dipilih."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Pilih soal terlebih dahulu!")
            return

        item = self.tree.item(selected_item[0])['values']
        EditQuestionWindow(self, item)

    def delete_question(self):
        """Menghapus soal yang dipilih."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Pilih soal terlebih dahulu!")
            return

        item = self.tree.item(selected_item[0])['values']
        with sqlite3.connect(self.app.DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM questions WHERE id = ?", (item[0],))
            conn.commit()

        self.tree.delete(selected_item[0])
        messagebox.showinfo("Info", "Soal berhasil dihapus!")

class AddQuestionWindow:
    def __init__(self, manage_window):
        self.manage_window = manage_window
        self.window = tk.Toplevel(manage_window.window)
        self.window.title("Tambah Soal")
        self.window.minsize(400, 300)

        ttk.Label(self.window, text="Soal:").pack(pady=5)
        self.entry_question = ttk.Entry(self.window)
        self.entry_question.pack(fill='x', padx=10)

        ttk.Label(self.window, text="Jawaban:").pack(pady=5)
        self.entry_answer = ttk.Entry(self.window)
        self.entry_answer.pack(fill='x', padx=10)

        ttk.Label(self.window, text="Opsi (pisahkan dengan koma):").pack(pady=5)
        self.entry_options = ttk.Entry(self.window)
        self.entry_options.pack(fill='x', padx=10)

        ttk.Button(self.window, text="Simpan", command=self.save_question).pack(pady=20)

    def save_question(self):
        """Menyimpan soal baru ke database."""
        question = self.entry_question.get().strip()
        answer = self.entry_answer.get().strip()
        options = self.entry_options.get().strip()

        if not question or not answer or not options:
            messagebox.showerror("Error", "Semua field harus diisi.")
            return

        with sqlite3.connect(self.manage_window.app.DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO questions (question, answer, options) VALUES (?, ?, ?)", (question, answer, options))
            conn.commit()

        messagebox.showinfo("Info", "Soal berhasil ditambahkan!")
        self.manage_window.load_questions()
        self.window.destroy()

class EditQuestionWindow:
    def __init__(self, manage_window, selected_question):
        self.manage_window = manage_window
        self.selected_question = selected_question
        self.window = tk.Toplevel(manage_window.window)
        self.window.title("Edit Soal")
        self.window.minsize(400, 300)

        ttk.Label(self.window, text="Edit Soal", font=("Arial", 14)).pack(pady=10)

        ttk.Label(self.window, text="Soal:").pack(pady=5)
        self.entry_question = ttk.Entry(self.window)
        self.entry_question.insert(0, selected_question[1])
        self.entry_question.pack(fill='x', padx=10)

        ttk.Label(self.window, text="Jawaban:").pack(pady=5)
        self.entry_answer = ttk.Entry(self.window)
        self.entry_answer.insert(0, selected_question[2])
        self.entry_answer.pack(fill='x', padx=10)

        ttk.Label(self.window, text="Opsi (pisahkan dengan koma):").pack(pady=5)
        self.entry_options = ttk.Entry(self.window)
        self.entry_options.insert(0, selected_question[3])
        self.entry_options.pack(fill='x', padx=10)

        ttk.Button(self.window, text="Simpan Perubahan", command=self.save_changes).pack(pady=20)

    def save_changes(self):
        """Menyimpan perubahan pada soal yang diedit."""
        question_id = self.selected_question[0]
        updated_question = self.entry_question.get().strip()
        updated_answer = self.entry_answer.get().strip()
        updated_options = self.entry_options.get().strip()

        if not updated_question or not updated_answer or not updated_options:
            messagebox.showerror("Error", "Semua field harus diisi.")
            return

        with sqlite3.connect(self.manage_window.app.DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE questions
                SET question = ?, answer = ?, options = ?
                WHERE id = ?
            """, (updated_question, updated_answer, updated_options, question_id))
            conn.commit()

        self.manage_window.load_questions()
        messagebox.showinfo("Sukses", "Soal berhasil diperbarui!")
        self.window.destroy()

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplikasi Pengelolaan Soal Kuis")
        self.root.minsize(400, 300)

        # Path database
        self.DATA_FOLDER = 'database'
        self.DB_PATH = os.path.join(self.DATA_FOLDER, 'questions.db')

        # Tombol untuk membuka pengelolaan soal
        ttk.Button(self.root, text="Kelola Soal", command=self.open_manage_questions).pack(pady=20)

    def open_manage_questions(self):
        """Membuka jendela pengelolaan soal."""
        ManageQuestionsWindow(self)

if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()


