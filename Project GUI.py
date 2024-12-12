import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import os

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplikasi Kuis - Login/Registrasi")
        self.root.geometry("300x200")
        self.root.resizable(False, False)

        # Inisialisasi Style
        self.style = ttk.Style()
        self.style.theme_use('clam')  # Anda bisa mengganti dengan 'default', 'alt', 'classic', dll.

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
        # Judul
        label_title = ttk.Label(self.root, text="Selamat Datang!", font=("Arial", 16))
        label_title.pack(pady=20)

        # Tombol Login dan Registrasi
        button_login = ttk.Button(self.root, text="Login", width=15, command=self.open_login_window)
        button_login.pack(pady=10)

        button_register = ttk.Button(self.root, text="Registrasi", width=15, command=self.open_register_window)
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
        self.register_window.geometry("350x300")
        self.register_window.resizable(False, False)

        # Inisialisasi Style untuk Window Registrasi
        self.style = ttk.Style()
        self.style.theme_use('clam')

        # Judul
        label_title = ttk.Label(self.register_window, text="Registrasi", font=("Arial", 16))
        label_title.pack(pady=10)

        # Frame registrasi
        frame_form = ttk.Frame(self.register_window)
        frame_form.pack(pady=10, padx=10, fill='x')

        # Username
        label_username = ttk.Label(frame_form, text="Username:")
        label_username.grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.entry_username = ttk.Entry(frame_form)
        self.entry_username.grid(row=0, column=1, padx=5, pady=5, sticky='w')

        # Password
        label_password = ttk.Label(frame_form, text="Password:")
        label_password.grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.entry_password = ttk.Entry(frame_form, show="*")
        self.entry_password.grid(row=1, column=1, padx=5, pady=5, sticky='w')

        # Konfirmasi Password
        label_confirm_password = ttk.Label(frame_form, text="Konfirmasi Password:")
        label_confirm_password.grid(row=2, column=0, padx=5, pady=5, sticky='e')
        self.entry_confirm_password = ttk.Entry(frame_form, show="*")
        self.entry_confirm_password.grid(row=2, column=1, padx=5, pady=5, sticky='w')

        # Submit
        button_submit = ttk.Button(self.register_window, text="Daftar", command=self.submit_registration)
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

        # Validasi karakter username (hanya huruf dan angka)
        if not username.isalnum():
            messagebox.showerror("Error", "Username hanya boleh mengandung huruf dan angka.")
            return

        try:
            with sqlite3.connect(self.app.DB_PATH) as conn:
                cursor = conn.cursor()
                cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
                conn.commit()
            messagebox.showinfo("Sukses", "Registrasi berhasil! Anda dapat login sekarang.")
            self.register_window.destroy()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username sudah digunakan. Silakan pilih username lain.")
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Terjadi kesalahan pada database: {e}")

class LoginWindow:
    def __init__(self, app):
        self.app = app
        self.login_window = tk.Toplevel(app.root)
        self.login_window.title("Login")
        self.login_window.geometry("350x250")
        self.login_window.resizable(False, False)

        # Buat container frame yang akan memenuhi window
        container = ttk.Frame(self.login_window)
        container.pack(expand=True, fill='both')  # Frame ini akan melebar dan memenuhi window

        # Judul
        label_title = ttk.Label(container, text="Login", font=("Arial", 16))
        label_title.pack(pady=10)

        # Frame untuk form login (jangan gunakan fill='x')
        frame_form = ttk.Frame(container)
        frame_form.pack(pady=10, padx=10)  # Tidak menggunakan fill='x', sehingga frame akan sesuai konten

        # Username
        label_username = ttk.Label(frame_form, text="Username:")
        label_username.grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.entry_username = ttk.Entry(frame_form)
        self.entry_username.grid(row=0, column=1, padx=5, pady=5)

        # Password
        label_password = ttk.Label(frame_form, text="Password:")
        label_password.grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.entry_password = ttk.Entry(frame_form, show="*")
        self.entry_password.grid(row=1, column=1, padx=5, pady=5)

        # Tombol Login
        button_login = ttk.Button(container, text="Login", command=self.submit_login)
        button_login.pack(pady=20)

    def submit_login(self):
        username = self.entry_username.get().strip()
        password = self.entry_password.get().strip()
        # Implementasi login Anda di sini
        # ...
        if username and password:
            messagebox.showinfo("Info", "Login dicoba!")
        else:
            messagebox.showerror("Error", "Semua field harus diisi.")

if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()
