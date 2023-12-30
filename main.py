import datetime
import sqlite3
import json
import random


class Expense:
    def __init__(self, title, amount, category, date=None):
        self.title = title
        self.date = date or datetime.datetime.now().strftime("%d/%m/%Y")
        self.amount = amount
        self.category = category

    def __str__(self):
        return f"New expense added on {self.date} of ₹{self.amount} in {self.category}"


def get_random_greeting():
    with open("greetings.json", "r") as file:
        greetings_data = json.load(file)
        greetings_list = greetings_data.get("greetings", [])
        return random.choice(greetings_list)


def insert_expense(cursor, expense):
    cursor.execute(
        "INSERT INTO expenses (title, date, amount, category) VALUES (?, ?, ?, ?)",
        (expense.title, expense.date, expense.amount, expense.category),
    )
    
    connection.commit()


def print_history(cursor):
    rows = cursor.execute("SELECT * FROM expenses").fetchall()

    if not rows:
        print("Empty! Add an expense to get started.")
    else:
        print("\nExpense History:")
        for row in rows:
            print(
                f"ID: {row[0]}, Title: {row[1]}, Date: {row[2]}, Amount: ₹{row[3]}, Category: {row[4]}"
            )

def delete_expense(cursor, id):
    
    
    cursor.execute("DELETE FROM expenses WHERE ID=?", (id,))
    
    cursor.execute("UPDATE expenses SET ID = ID - 1 WHERE ID > ?", (id,))
    
    cursor.execute("UPDATE SQLITE_SEQUENCE SET SEQ=SEQ-1 WHERE NAME='expenses'")
    
    connection.commit()



try:
    connection = sqlite3.connect("expenses.db")
    cursor = connection.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS expenses (ID INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, date TEXT, amount REAL, category TEXT)"
    )

    print(get_random_greeting())
    print("-------------------------------")

    while True:
        print("\nWhat do you want to do? (Enter the number)")
        print("1. Add Expense")
        print("2. Print Expense History")
        print("3. Delete Expense")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            title = input("\nEnter the title of the expense: ")
            while True:
                amount = input("Enter the amount of the expense: ")
                try:
                    amount = float(amount)
                    break
                except ValueError:
                    print("Invalid amount. Please enter a number.")
            category = input("Enter the category of the expense: ")

            new_expense = Expense(title, amount, category)
            insert_expense(cursor, new_expense)

            print("\n" + str(new_expense))

        elif choice == "2":
            print_history(cursor)

        elif choice == "3":
            print_history(cursor)
            id_to_delete = input("\nEnter the ID of the expense to delete: ")
            delete_expense(cursor, id_to_delete)
            print("\nExpense deleted successfully!")

        elif choice == "4":
            print("\nExiting...")
            break

        else:
            print("Invalid choice. Please try again.")

except KeyboardInterrupt:
    print("\nExiting...")

finally:
    connection.close()