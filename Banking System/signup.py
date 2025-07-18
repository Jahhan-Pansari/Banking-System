import tkinter as tk
from tkinter import messagebox
import sqlite3

def signup():
    username = entry_new_username.get()
    password = entry_new_password.get()

    if username == '' or password == '':
        messagebox.showerror("Sign-up Failed", "Username and password cannot be empty")
    else:
        if create_user(username, password):
            messagebox.showinfo("Sign-up Successful", "Account created successfully")
        else:
            messagebox.showerror("Sign-up Failed", "Username already exists")

def create_user(username, password):
    conn = sqlite3.connect('users2.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=?", (username,))
    existing_user = c.fetchone()
    if existing_user:
        conn.close()
        return False
    else:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        conn.close()
        return True

root = tk.Tk()
root.title("Sign Up")
root.geometry("250x110")

label_new_username = tk.Label(root, text="New Username:")
label_new_password = tk.Label(root, text="New Password:")
entry_new_username = tk.Entry(root)
entry_new_password = tk.Entry(root, show="*")
button_signup = tk.Button(root, text="Sign Up", command=signup)

label_new_username.grid(row=0, column=0, sticky="w", padx=10, pady=5)
label_new_password.grid(row=1, column=0, sticky="w", padx=10, pady=5)
entry_new_username.grid(row=0, column=1, padx=10, pady=5)
entry_new_password.grid(row=1, column=1, padx=10, pady=5)
button_signup.grid(row=2, columnspan=2, pady=10)

root.mainloop()
