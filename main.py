import datetime
import sqlite3
import json
import random


# Initializing the database
connection = sqlite3.connect("expenses.db")
cursor = connection.cursor()




class Expense:
    def __init__(self, title, amount, category):
        current_time = datetime.datetime.now()
        self.title = title
        self.date = current_time.strftime("%d/%m/%Y")
        self.amount = amount
        self.category = category

    def __str__(self):
        return f"New expense added on {self.date} of ₹{self.amount} in {self.category}"


def get_random_greeting():
    with open("greetings.json", "r") as file:
        greetings_data = json.load(file)
        greetings_list = greetings_data.get("greetings", [])
        return random.choice(greetings_list)


try:

    print(get_random_greeting())
    print("-------------------------------")


    while True:
        title = input("\nEnter the title of the expense: ")
        amount = input("Enter the amount of the expense: ")
        category = input("Enter the category of the expense: ")

        new_expense = Expense(title, amount, category)

        e_title = new_expense.title
        e_date = new_expense.date
        e_amount = new_expense.amount
        e_category = new_expense.category

        cursor.execute("CREATE TABLE IF NOT EXISTS expenses (ID INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, date TEXT, amount REAL, category TEXT)")
        cursor.execute("INSERT INTO expenses (title, date, amount, category) VALUES (?, ?, ?, ?)", (e_title, e_date, e_amount, e_category))

        rows = cursor.execute("SELECT * FROM expenses").fetchall()
        print("\nExpense History:")
        for row in rows:
            print(f"ID: {row[0]}, Title: {row[1]}, Date: {row[2]}, Amount: ₹{row[3]}, Category: {row[4]}")

        print("\n" + str(new_expense))

        connection.commit()

        add_new = input("Do you want to add another expense? (yes/no): ")
        if add_new.lower() != 'yes':
            print("\nExiting...")
            break

except KeyboardInterrupt:
    print("\nExiting...")

finally:
    connection.close()
