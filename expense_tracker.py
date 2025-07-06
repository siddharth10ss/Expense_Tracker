"""
Command-Line Expense Tracker

Features:
- Add expenses with date, amount, category, and description.
- Save expenses in a local CSV file.
- Display all expenses in a readable format.
- Generate and display monthly totals per category.
- Plot pie chart or bar chart of expenses by category for a selected month using matplotlib.
- Includes basic error handling and clear comments.
"""

import csv
import os
from datetime import datetime
from collections import defaultdict
import matplotlib.pyplot as plt

CSV_FILE = "expenses.csv"
FIELDNAMES = ["date", "amount", "category", "description"]

def initialize_csv():
    """Create the CSV file with headers if it doesn't exist."""
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
            writer.writeheader()

def add_expense():
    """Add a new expense entry."""
    try:
        date_str = input("Enter date (YYYY-MM-DD): ").strip()
        # Validate date format
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        amount_str = input("Enter amount: ").strip()
        amount = float(amount_str)
        category = input("Enter category: ").strip()
        description = input("Enter description: ").strip()

        with open(CSV_FILE, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
            writer.writerow({
                "date": date_obj.strftime("%Y-%m-%d"),
                "amount": f"{amount:.2f}",
                "category": category,
                "description": description
            })
        print("Expense added successfully.")
    except ValueError as ve:
        print(f"Invalid input: {ve}. Please try again.")
    except Exception as e:
        print(f"Error adding expense: {e}")

def read_expenses():
    """Read all expenses from the CSV file."""
    expenses = []
    if not os.path.exists(CSV_FILE):
        return expenses
    try:
        with open(CSV_FILE, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Convert amount to float and date to datetime object
                try:
                    row["amount"] = float(row["amount"])
                    row["date"] = datetime.strptime(row["date"], "%Y-%m-%d")
                    expenses.append(row)
                except Exception:
                    # Skip malformed rows
                    continue
    except Exception as e:
        print(f"Error reading expenses: {e}")
    return expenses

def display_expenses():
    """Display all expenses in a readable format."""
    expenses = read_expenses()
    if not expenses:
        print("No expenses found.")
        return
    print(f"\n{'Date':<12} {'Amount':>10} {'Category':<15} Description")
    print("-" * 55)
    for exp in expenses:
        date_str = exp["date"].strftime("%Y-%m-%d")
        amount_str = f"${exp['amount']:.2f}"
        print(f"{date_str:<12} {amount_str:>10} {exp['category']:<15} {exp['description']}")
    print()

def monthly_totals():
    """Generate and display monthly totals per category."""
    expenses = read_expenses()
    if not expenses:
        print("No expenses found.")
        return
    totals = defaultdict(lambda: defaultdict(float))  # totals[month][category] = amount
    for exp in expenses:
        month = exp["date"].strftime("%Y-%m")
        totals[month][exp["category"]] += exp["amount"]

    print("\nMonthly Totals per Category:")
    for month in sorted(totals.keys()):
        print(f"\n{month}:")
        for category, amount in totals[month].items():
            print(f"  {category:<15} : ${amount:.2f}")
    print()

def plot_expenses():
    """Plot a pie or bar chart of expenses by category for a selected month."""
    expenses = read_expenses()
    if not expenses:
        print("No expenses found.")
        return
    month_input = input("Enter month to plot (YYYY-MM): ").strip()
    try:
        datetime.strptime(month_input, "%Y-%m")
    except ValueError:
        print("Invalid month format. Use YYYY-MM.")
        return

    # Filter expenses for the selected month
    filtered = [exp for exp in expenses if exp["date"].strftime("%Y-%m") == month_input]
    if not filtered:
        print(f"No expenses found for {month_input}.")
        return

    # Aggregate amounts by category
    category_totals = defaultdict(float)
    for exp in filtered:
        category_totals[exp["category"]] += exp["amount"]

    categories = list(category_totals.keys())
    amounts = list(category_totals.values())

    print("Choose chart type:")
    print("1. Pie Chart")
    print("2. Bar Chart")
    choice = input("Enter choice (1 or 2): ").strip()

    plt.figure(figsize=(8,6))
    if choice == "1":
        plt.pie(amounts, labels=categories, autopct='%1.1f%%', startangle=140)
        plt.title(f"Expenses by Category for {month_input}")
    elif choice == "2":
        plt.bar(categories, amounts, color='skyblue')
        plt.title(f"Expenses by Category for {month_input}")
        plt.ylabel("Amount ($)")
        plt.xticks(rotation=45, ha='right')
    else:
        print("Invalid choice.")
        return

    plt.tight_layout()
    plt.show()

def main():
    initialize_csv()
    while True:
        print("Expense Tracker Menu:")
        print("1. Add Expense")
        print("2. Display All Expenses")
        print("3. Show Monthly Totals per Category")
        print("4. Plot Expenses by Category for a Month")
        print("5. Exit")
        choice = input("Enter your choice (1-5): ").strip()

        if choice == "1":
            add_expense()
        elif choice == "2":
            display_expenses()
        elif choice == "3":
            monthly_totals()
        elif choice == "4":
            plot_expenses()
        elif choice == "5":
            print("Exiting Expense Tracker. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")

if __name__ == "__main__":
    main()
