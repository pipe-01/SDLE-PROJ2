import sqlite3
import os.path
import os.path


class Database:

    def __init__(self, ip, port):
        #db_filepath = os.path.join("C:\\Users\\mika1\\Desktop\\Filipe\\proj2\\db", "users_{0}_{1}.db".format(ip, port))
        db_filepath = os.path.join("db", "users_{0}_{1}.db".format(ip, port))
        self.connection = sqlite3.connect(db_filepath, check_same_thread=False, isolation_level=None)
        self.cur = self.connection.cursor()
        if os.path.exists(db_filepath):
            self.create_user_table()

    def insert(self, username, password):
        self.cur.execute("INSERT INTO users VALUES (?, ?)", (username, password))
        self.connection.commit()

    def search(self, username):
        self.cur.execute("SELECT password FROM users WHERE username=?", (username,))
        users = self.cur.fetchone()
        return users

    def view(self):
        self.cur.execute("SELECT * FROM users")
        rows = self.cur.fetchall()
        return rows

    def delete(self, username):
        self.cur.execute("DELETE FROM users WHERE username=?", (username,))
        self.connection.commit()

    def update(self, username, password):
        self.cur.execute("UPDATE users SET password=? WHERE username=?", (password, username))
        self.connection.commit()

    def __del__(self):
        self.connection.close()

    def create_user_table(self):
        self.cur.execute("""CREATE TABLE IF NOT EXISTS users (username 
        text PRIMARY KEY UNIQUE, password text NOT NULL)""")
