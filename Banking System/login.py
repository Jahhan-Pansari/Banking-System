import tkinter as tk
from tkinter import messagebox
import sqlite3
import subprocess

def login():
    global username, password
    username = entry_username.get()
    password = entry_password.get()

    with open("username.txt", "w") as file:
        file.truncate()
        file.write(username)

    if authenticate_user(username, password):
        messagebox.showinfo("Login Successful", "Welcome, " + username)
        subprocess.run(["python", "bank.py"])
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")

def authenticate_user(username, password):
    conn = sqlite3.connect('users2.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = c.fetchone()
    conn.close()
    return user is not None

root = tk.Tk()
root.title("Login")

label_username = tk.Label(root, text="Username:")
label_password = tk.Label(root, text="Password:")
entry_username = tk.Entry(root)
entry_password = tk.Entry(root, show="*")
button_login = tk.Button(root, text="Login", command=login)

label_username.grid(row=0, column=0)
label_password.grid(row=1, column=0)
entry_username.grid(row=0, column=1)
entry_password.grid(row=1, column=1)
button_login.grid(row=2, columnspan=2)

root.mainloop()
