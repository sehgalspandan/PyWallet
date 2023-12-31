import locale
import datetime
import sqlite3
import json
import random

# Set the locale for formatting
locale.setlocale(locale.LC_ALL, '')

class Expense:
    def __init__(self, title, amount, category, date=None):
        self.title = title
        self.date = date or datetime.datetime.now().strftime("%d/%m/%Y")
        self.amount = amount
        self.category = category

    def __str__(self):
        formatted_amount = locale.format_string("%.2f", self.amount, grouping=True)
        return f"New expense added on {self.date} of ₹{formatted_amount} in {self.category}"

# Rest of your script remains unchanged


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
        print("\nExpense History:\n")
        for row in rows:
            formatted_amount = locale.format_string("%.2f", row[3], grouping=True)
            print(
                f"ID: {row[0]}, Title: {row[1]}, Date: {row[2]}, Amount: ₹{formatted_amount}, Category: {row[4]}"
            )

        total = cursor.execute("SELECT SUM(amount) FROM expenses").fetchone()[0]
        formatted_total = locale.format_string("%.2f", total, grouping=True)
        print(f"\nTotal: ₹{formatted_total}")

def delete_expense(cursor, id):
    
    
    cursor.execute("DELETE FROM expenses WHERE ID=?", (id,))
    
    cursor.execute("UPDATE expenses SET ID = ID - 1 WHERE ID > ?", (id,))
    
    cursor.execute("UPDATE SQLITE_SEQUENCE SET SEQ=SEQ-1 WHERE NAME='expenses'")
    
    connection.commit()


def get_expense(cursor, id):
    cursor.execute("SELECT * FROM expenses WHERE ID=?", (id,))
    row = cursor.fetchone()
    formatted_amount = locale.format_string("%.2f", row[3], grouping=True)
    print(f"\nID: {row[0]}, Title: {row[1]}, Date: {row[2]}, Amount: ₹{formatted_amount}, Category: {row[4]}")
    

def edit_expense(cursor, id):
    get_expense(cursor, id)
    
    field_to_edit = input("\nWhat do you want to edit? (Enter the number) \n1. Title \n2. Date \n3. Amount \n4. Category \nEnter your choice:")
    if field_to_edit == "1":
        title = input("\nEnter the new title: ")
        cursor.execute("UPDATE expenses SET title = ? WHERE id = ?", (title, id) )
        connection.commit()
        print("\nTitle updated successfully!")
        print ("\nUpdated Expense: ")
        get_expense(cursor, id)

    elif field_to_edit == "2":
        date = input("\nEnter the new date (dd/mm/yyyy): ")
        cursor.execute("UPDATE expenses SET date = ? WHERE id = ?", (date, id) )
        connection.commit()
        print("\nDate updated successfully!")
        print ("\nUpdated Expense: ")
        get_expense(cursor, id)

    elif field_to_edit == "3":
        amount = input("\nEnter the new amount: ")
        cursor.execute("UPDATE expenses SET amount = ? WHERE id = ?", (amount, id) )
        connection.commit()
        print("\nAmount updated successfully!")
        print ("\nUpdated Expense: ")
        get_expense(cursor, id)

    elif field_to_edit == "4":
        category = input("\nEnter the new category: ")
        cursor.execute("UPDATE expenses SET category = ? WHERE id = ?", (category, id) )
        connection.commit()
        print("\nCategory updated successfully!")
        print ("\nUpdated Expense: ")
        get_expense(cursor, id)

    else:
        print("Invalid choice. Please try again.")



try:
    connection = sqlite3.connect("expenses.db")
    cursor = connection.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS expenses (ID INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, date TEXT, amount REAL, category TEXT)"
    )

    print(get_random_greeting())
    print("-------------------------------")
    print("Note: You can press Ctrl+C to exit/stop operation at any time.")

    while True:
        print("\nWhat do you want to do? (Enter the number)")
        print("1. Add Expense")
        print("2. Print Expense History")
        print("3. Delete Expense")
        print("4. Edit Expense")
        print("5. Exit")

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
            print_history(cursor)
            id_to_edit = input("\nEnter the ID of the expense to edit: ")
            edit_expense(cursor, id_to_edit)
            

        elif choice == "5" or choice.lower() == "exit":
            print("\nExiting...")
            break

        else:
            print("Invalid choice. Please try again.")

except KeyboardInterrupt:
    print("\nExiting...")

finally:
    connection.close()