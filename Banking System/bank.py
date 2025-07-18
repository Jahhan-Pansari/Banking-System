import tkinter as tk
from tkinter import messagebox
import sqlite3

with open("username.txt", "r") as file:
    username = file.read()
    print(username)

def get_user_data(username):
    conn = sqlite3.connect('users2.db')
    cursor = conn.cursor()

    cursor.execute("SELECT currentBalance, TotalDeposit, TotalWidthdraw FROM users WHERE username=?", (username,))
    result = cursor.fetchone()

    conn.close()

    if result is not None:
        logcurrent_balance, logtotal_deposits, logtotal_withdrawals = result
        return logcurrent_balance, logtotal_deposits, logtotal_withdrawals
    else:
        return None

user_data = get_user_data(username)

if user_data is not None:
    logcurrent_balance, logtotal_deposits, logtotal_withdrawals = user_data
    print(f"Current balance: {logcurrent_balance}")
    print(f"Total deposits: {logtotal_deposits}")
    print(f"Total withdrawals: {logtotal_withdrawals}")
else:
    print(f"No user found with username {username}")

current_balance = logcurrent_balance
total_deposits = logtotal_deposits
total_withdrawals = logtotal_withdrawals

def update_user_data(name, current_balance, total_deposit, total_withdraw):
    try:
        conn = sqlite3.connect('users2.db')
        cursor = conn.cursor()

        cursor.execute("UPDATE users SET currentBalance=?, TotalDeposit=?, TotalWidthdraw=? WHERE username=?", 
                        (current_balance, total_deposit, total_withdraw, name))
        conn.commit()

        print("User data updated successfully.")

    except sqlite3.Error as e:
        print("Error updating user data:", e)

    finally:
        conn.close()


def update_user_history(namedef, type_of_transactiondef, amountdef, balancedef):
    global trans_type, username, amount_for_history, current_balance
    with open("username.txt", "r") as file:
        username = file.read()
        print(username)
    try:
        conn = sqlite3.connect('users2.db')
        cursor = conn.cursor()
        
        from datetime import datetime
        current_datetime = datetime.now()
        formatted_date = current_datetime.strftime("%d/%m/%Y")
    
        now = datetime.now()
        formatted_time = now.strftime("%H:%M:%S")

        cursor.execute('''CREATE TABLE IF NOT EXISTS transactions
             (username TEXT, transaction_type TEXT, amount INTEGER, balance INTEGER, date TEXT, time TEXT)''')

        sql_command = ('''INSERT INTO transactions (username, transaction_type, amount, balance, date, time) 
               VALUES (?, ?, ?, ?, ?, ?)''')
        cursor.execute(sql_command, (namedef, type_of_transactiondef, amountdef, balancedef, formatted_date, formatted_time))
        conn.commit()

        print("User data updated successfully.")

    except sqlite3.Error as e:
        print("Error updating user data:", e)


def check_balance():
    messagebox.showinfo("Balance", "Balance in account: " + str(current_balance))

def deposit_money():
    deposit_window = tk.Toplevel()
    deposit_window.title("Deposit Money")
    deposit_window.geometry("500x150")

    deposit_label = tk.Label(deposit_window, text="Enter the amount you want to deposit:", font=("Arial", 14))
    deposit_label.grid(row=0, columnspan=2, padx=10, pady=10)

    deposit_entry = tk.Entry(deposit_window, font=("Arial", 14))
    deposit_entry.grid(row=1, columnspan=2, padx=10, pady=10)

    def deposit():
        global current_balance, total_deposits, total_withdrawals, username, trans_type
        value_deposit = int(deposit_entry.get())
        current_balance += value_deposit
        total_deposits += 1
        trans_type = "Deposited"
        update_user_history(username, trans_type, value_deposit, current_balance)
        balance_label.config(text=f"Balance: ${current_balance}")
        total_deposits_label.config(text=f"Total Deposits: {total_deposits}")
        last_transaction_label.config(text="Last Transaction: Deposited " + str(value_deposit))
        with open("username.txt", "r") as file:
            username = file.read()
            print(username)
        update_user_data(username, current_balance, total_deposits, total_withdrawals)

        deposit_window.destroy()

    deposit_button = tk.Button(deposit_window, text="Deposit", font=("Arial", 14), width=20, command=deposit)
    deposit_button.grid(row=2, column=0, padx=10, pady=10)

    cancel_button = tk.Button(deposit_window, text="Cancel", font=("Arial", 14), width=20, command=deposit_window.destroy)
    cancel_button.grid(row=2, column=1, padx=10, pady=10)

if current_balance == None:
    current_balance = 0
if total_deposits == None:
    total_deposits = 0
if total_withdrawals == None:
    total_withdrawals = 0

root = tk.Tk()
root.title("Python Bank Of India")
root.geometry("500x375")

balance_label = tk.Label(root, text=f"Balance: ${current_balance}", font=("Arial", 16))
balance_label.grid(row=0, columnspan=2, padx=10, pady=10)

last_transaction_label = tk.Label(root, text="Last Transaction: None", font=("Arial", 12))
last_transaction_label.grid(row=1, columnspan=2, padx=10, pady=5)

total_deposits_label = tk.Label(root, text=f"Total Deposits: {total_deposits}", font=("Arial", 12))
total_deposits_label.grid(row=2, columnspan=2, padx=10, pady=5)

total_withdrawals_label = tk.Label(root, text=f"Total Withdrawals: {total_withdrawals}", font=("Arial", 12))
total_withdrawals_label.grid(row=3, columnspan=2, padx=10, pady=5)

check_balance_button = tk.Button(root, text="Check Balance", font=("Arial", 14), width=20, command=check_balance)
check_balance_button.grid(row=4, column=0, padx=10, pady=10)

deposit_money_button = tk.Button(root, text="Deposit Money", font=("Arial", 14), width=20, command=deposit_money)
deposit_money_button.grid(row=4, column=1, padx=10, pady=10)

def withdraw_money():
    # Create a new window for withdrawal
    withdrawal_window = tk.Toplevel()
    withdrawal_window.title("Withdraw Money")
    withdrawal_window.geometry("500x150")

    withdrawal_label = tk.Label(withdrawal_window, text="Enter the amount you want to withdraw:", font=("Arial", 14))
    withdrawal_label.grid(row=0, columnspan=2, padx=10, pady=10)

    withdrawal_entry = tk.Entry(withdrawal_window, font=("Arial", 14))
    withdrawal_entry.grid(row=1, columnspan=2, padx=10, pady=10)

    def withdraw():
        global withdrawal_amount, total_deposits, total_withdrawals, current_balance, username
        withdrawal_amount = float(withdrawal_entry.get())

        if withdrawal_amount > current_balance:
            print("Insufficient balance!")
            messagebox.showerror("Insufficient balance!", "You do not have enough money in your account.")
        else:
            total_withdrawals += 1
            current_balance -= withdrawal_amount

            trans_type = "Withdrawed"
            update_user_history(username, trans_type, withdrawal_amount, current_balance)
            total_withdrawals_label.config(text=f"Total Withdrawals: {total_withdrawals}")
            balance_label.config(text=f"Balance: ${current_balance}")
            last_transaction_label.config(text="Last Transaction: Withdrawed " + str(withdrawal_amount))
            with open("username.txt", "r") as file:
                username = file.read()
                print(username)
            update_user_data(username, current_balance, total_deposits, total_withdrawals)
            withdrawal_window.destroy()

    withdraw_button = tk.Button(withdrawal_window, text="Withdraw", font=("Arial", 14), width=20, command=withdraw)
    withdraw_button.grid(row=2, column=0, padx=10, pady=10)

    cancel_button = tk.Button(withdrawal_window, text="Cancel", font=("Arial", 14), width=20, command=withdrawal_window.destroy)
    cancel_button.grid(row=2, column=1, padx=10, pady=10)

withdraw_money_button = tk.Button(root, text="Withdraw Money", font=("Arial", 14), width=20, command=withdraw_money)
withdraw_money_button.grid(row=5, column=0, padx=10, pady=10)

withdraw_money_button.config(command=lambda: withdraw_money())

def trans_history():
    global username
    conn = sqlite3.connect('users2.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM transactions WHERE username=?", (username,))
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    with open('transaction_history.txt', 'w') as file:
        file.write("Username  TransactionType  Amount  - Balance  Date  Time" + "\n")
        for row in rows:
            file.write('\t'.join(map(str, row)) + '\n')


transaction_history_button = tk.Button(root, text="Transaction History", font=("Arial", 14), width=20, command=trans_history)
transaction_history_button.grid(row=5, column=1, padx=10, pady=10)

quit_entry = tk.Entry(root, font=("Arial", 14))
quit_entry.grid(row=6, columnspan=2, padx=10, pady=10)

def quit_command():
    global current_balance, total_deposits, total_withdrawals
    name = quit_entry.get()
    update_user_data(name, current_balance, total_deposits, total_withdrawals)
    root.quit()

exit_button = tk.Button(root, text="Quit", font=("Arial", 14), width=20, command=quit_command)
exit_button.grid(row=7, columnspan=2, padx=10, pady=10)

root.mainloop()