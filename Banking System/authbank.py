import sqlite3
def get_user_data(username):
    conn = sqlite3.connect('users2.db')
    cursor = conn.cursor()

    cursor.execute("SELECT currentBalance, TotalDeposit, TotalWidthdraw FROM users WHERE username=?", (username,))
    result = cursor.fetchone()

    conn.close()

    if result is not None:
        current_balance, total_deposits, total_withdrawals = result
        return current_balance, total_deposits, total_withdrawals
    else:
        return None

# Example usage
username = input("Enter your username: ")
user_data = get_user_data(username)

if user_data is not None:
    current_balance, total_deposits, total_withdrawals = user_data
    print(f"Current balance: {current_balance}")
    print(f"Total deposits: {total_deposits}")
    print(f"Total withdrawals: {total_withdrawals}")
else:
    print(f"No user found with username {username}")