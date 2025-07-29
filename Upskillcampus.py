import sqlite3
from cryptography.fernet import Fernet
import os

# ====== Setup ======

# Generate key (run once and reuse)
def generate_key():
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)

# Load key
def load_key():
    return open("key.key", "rb").read()

# Create database if it doesn't exist
def init_db():
    conn = sqlite3.connect("passwords.db")
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS passwords (
                    account TEXT,
                    username TEXT,
                    password TEXT
                )""")
    conn.commit()
    conn.close()

# ====== Main Functions ======

def add_password(account, username, password):
    key = load_key()
    fernet = Fernet(key)
    encrypted_pw = fernet.encrypt(password.encode())

    conn = sqlite3.connect("passwords.db")
    c = conn.cursor()
    c.execute("INSERT INTO passwords VALUES (?, ?, ?)", (account, username, encrypted_pw))
    conn.commit()
    conn.close()
    print("Password added successfully!")

def view_password(account_name):
    key = load_key()
    fernet = Fernet(key)

    conn = sqlite3.connect("passwords.db")
    c = conn.cursor()
    c.execute("SELECT username, password FROM passwords WHERE account=?", (account_name,))
    result = c.fetchone()
    conn.close()

    if result:
        username, encrypted_pw = result
        decrypted_pw = fernet.decrypt(encrypted_pw).decode()
        print(f"\n Account: {account_name}")
        print(f"Username: {username}")
        print(f"Password: {decrypted_pw}\n")
    else:
        print("No entry found for that account.")

# ====== CLI Interface ======

def main():
    if not os.path.exists("key.key"):
        generate_key()
        print("Encryption key generated.")

    init_db()

    while True:
        print("\n====== Password Manager ======")
        print("1. Add New Password")
        print("2. View Password")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            acc = input("Enter Account Name (e.g., Gmail): ")
            user = input("Enter Username: ")
            pw = input("Enter Password: ")
            add_password(acc, user, pw)

        elif choice == "2":
            acc = input("Enter Account Name to search: ")
            view_password(acc)

        elif choice == "3":
            print("Exiting Password Manager.")
            break
        else:
            print("Invalid choice. Please try again.")

# ====== Run ======
if __name__ == "__main__":
    main()
