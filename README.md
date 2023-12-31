# Expense Tracker

This Python project is an expense tracker that allows users to add, view, and delete expenses. It uses SQLite for database storage and provides a command-line interface for interaction.

## Features

1. **Add Expense**: Users can add new expenses by providing a title, amount, and category.
2. **Print Expense History**: View the history of all expenses, including their details such as ID, title, date, amount, and category.
3. **Delete Expense**: Remove an expense from the history by specifying its ID.

## Getting Started

### Prerequisites

Make sure you have Python installed on your system.

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/sehgalspandan/PyWallet.git
   ```

2. Navigate to the project directory:

   ```bash
   cd PyWallet
   ```

3. Run the script:

   ```bash
   python main.py
   ```

## Usage

1. Choose the appropriate option by entering the corresponding number.
2. Follow the prompts to add, view, or delete expenses.

## Files

- **`main.py`**: The main Python script containing the Expense class and the logic for user interaction.
- **`greetings.json`**: A JSON file containing a list of greetings used randomly.
- **`expenses.db`**: SQLite database file storing the expenses. (Note: This file is created automatically when the script is run for the first time. It is not included in the repository.)

## Acknowledgments

- This project was inspired by the need for a simple command-line expense tracker.

## Tech Stack

- Python
- Sqlite3
