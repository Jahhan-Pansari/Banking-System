import tkinter as tk
import subprocess
import sqlite3

conn = sqlite3.connect('users2.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users
             (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT, currentBalance INTEGER, TotalDeposit INTEGER, TotalWidthdraw INTEGER)''')
conn.commit()
conn.close()

def open_signup():
    subprocess.run(["python", "signup.py"])
    root.destroy()

def open_login():
    subprocess.run(["python", "login.py"])
    root.destroy()

root = tk.Tk()
root.title("Python Bank Of India")
root.geometry("300x250")
root.configure(bg="#f0f0f0")

label_heading = tk.Label(root, text="Bank", font=("Arial", 32), bg="#f0f0f0", fg="#333333")
label_heading.pack(pady=20)

button_signup = tk.Button(root, text="Sign Up", width=20, font=("Arial", 14), bg="#4CAF50", fg="white", command=open_signup)
button_signup.pack(pady=10)

button_login = tk.Button(root, text="Login", width=20, font=("Arial", 14), bg="#008CBA", fg="white", command=open_login)
button_login.pack(pady=10)

root.mainloop()
