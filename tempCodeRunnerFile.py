
        password = self.entry_password.get().strip()

        try:
            with sqlite3.connect(self.app.DB_PATH) as conn:
                cursor = conn.cursor()
                cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
                conn.commit()
            messagebox.showinfo("Sukses", "Registrasi berhasil! Anda dapat login sekarang.")
            self.register_window.destroy()
        except sqlite3.IntegrityError:
            logging.error("Username sudah ada di database")
            messagebox.showerror("Error", "Username anda sudah digunakan. Silahkan gunakan username lain")
        except sqlite3.Error as e: