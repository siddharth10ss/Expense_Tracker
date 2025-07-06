"""
Tkinter GUI Expense Tracker

Features:
- Add expenses with date, amount, category, and description.
- Save expenses in a local CSV file.
- Display all expenses in a readable table.
- Generate and display monthly totals per category.
- Plot pie chart or bar chart of expenses by category for a selected month using matplotlib.
- Basic error handling and clear comments.
"""

import csv
import os
from datetime import datetime
from collections import defaultdict
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import matplotlib.pyplot as plt

CSV_FILE = "expenses.csv"
FIELDNAMES = ["date", "amount", "category", "description"]

class ExpenseTrackerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Expense Tracker")
        self.geometry("800x600")
        self.create_widgets()
        self.initialize_csv()
        self.load_expenses()

    def initialize_csv(self):
        """Create the CSV file with headers if it doesn't exist."""
        if not os.path.exists(CSV_FILE):
            with open(CSV_FILE, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
                writer.writeheader()

    def create_widgets(self):
        # Frame for adding expenses
        add_frame = ttk.LabelFrame(self, text="Add Expense")
        add_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(add_frame, text="Date (YYYY-MM-DD):").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.date_entry = ttk.Entry(add_frame)
        self.date_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(add_frame, text="Amount:").grid(row=0, column=2, padx=5, pady=5, sticky="e")
        self.amount_entry = ttk.Entry(add_frame)
        self.amount_entry.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(add_frame, text="Category:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.category_entry = ttk.Entry(add_frame)
        self.category_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(add_frame, text="Description:").grid(row=1, column=2, padx=5, pady=5, sticky="e")
        self.description_entry = ttk.Entry(add_frame)
        self.description_entry.grid(row=1, column=3, padx=5, pady=5)

        add_button = ttk.Button(add_frame, text="Add Expense", command=self.add_expense)
        add_button.grid(row=2, column=0, columnspan=4, pady=10)

        # Frame for displaying expenses
        display_frame = ttk.LabelFrame(self, text="All Expenses")
        display_frame.pack(fill="both", expand=True, padx=10, pady=5)

        columns = ("date", "amount", "category", "description")
        self.tree = ttk.Treeview(display_frame, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col.capitalize())
            self.tree.column(col, anchor="center")
        self.tree.pack(fill="both", expand=True)

        # Frame for monthly totals and plotting
        bottom_frame = ttk.Frame(self)
        bottom_frame.pack(fill="x", padx=10, pady=5)

        totals_button = ttk.Button(bottom_frame, text="Show Monthly Totals", command=self.show_monthly_totals)
        totals_button.pack(side="left", padx=5)

        plot_button = ttk.Button(bottom_frame, text="Plot Expenses", command=self.plot_expenses)
        plot_button.pack(side="left", padx=5)

    def add_expense(self):
        date_str = self.date_entry.get().strip()
        amount_str = self.amount_entry.get().strip()
        category = self.category_entry.get().strip()
        description = self.description_entry.get().strip()

        # Validate inputs
        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Invalid Date", "Date must be in YYYY-MM-DD format.")
            return
        try:
            amount = float(amount_str)
        except ValueError:
            messagebox.showerror("Invalid Amount", "Amount must be a number.")
            return
        if not category:
            messagebox.showerror("Invalid Category", "Category cannot be empty.")
            return

        # Save to CSV
        try:
            with open(CSV_FILE, mode='a', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
                writer.writerow({
                    "date": date_obj.strftime("%Y-%m-%d"),
                    "amount": f"{amount:.2f}",
                    "category": category,
                    "description": description
                })
            messagebox.showinfo("Success", "Expense added successfully.")
            self.clear_entries()
            self.load_expenses()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add expense: {e}")

    def clear_entries(self):
        self.date_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)
        self.category_entry.delete(0, tk.END)
        self.description_entry.delete(0, tk.END)

    def load_expenses(self):
        # Clear current treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        # Load expenses from CSV
        if not os.path.exists(CSV_FILE):
            return
        try:
            with open(CSV_FILE, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    self.tree.insert("", tk.END, values=(
                        row["date"],
                        f"₹{float(row['amount']):.2f}",
                        row["category"],
                        row["description"]
                    ))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load expenses: {e}")

    def show_monthly_totals(self):
        expenses = self.read_expenses()
        if not expenses:
            messagebox.showinfo("No Data", "No expenses found.")
            return
        totals = defaultdict(lambda: defaultdict(float))
        for exp in expenses:
            month = exp["date"].strftime("%Y-%m")
            totals[month][exp["category"]] += exp["amount"]

        # Format output string
        output = ""
        for month in sorted(totals.keys()):
            output += f"{month}:\n"
            for category, amount in totals[month].items():
                output += f"  {category}: ₹{amount:.2f}\n"
            output += "\n"

        # Show in a popup window
        top = tk.Toplevel(self)
        top.title("Monthly Totals per Category")
        text = tk.Text(top, width=50, height=20)
        text.pack(padx=10, pady=10)
        text.insert(tk.END, output)
        text.config(state=tk.DISABLED)

    def read_expenses(self):
        expenses = []
        if not os.path.exists(CSV_FILE):
            return expenses
        try:
            with open(CSV_FILE, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    try:
                        row["amount"] = float(row["amount"])
                        row["date"] = datetime.strptime(row["date"], "%Y-%m-%d")
                        expenses.append(row)
                    except Exception:
                        continue
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read expenses: {e}")
        return expenses

    def plot_expenses(self):
        expenses = self.read_expenses()
        if not expenses:
            messagebox.showinfo("No Data", "No expenses found.")
            return
        month_input = simpledialog.askstring("Input", "Enter month to plot (YYYY-MM):", parent=self)
        if not month_input:
            return
        try:
            datetime.strptime(month_input, "%Y-%m")
        except ValueError:
            messagebox.showerror("Invalid Input", "Month must be in YYYY-MM format.")
            return

        filtered = [exp for exp in expenses if exp["date"].strftime("%Y-%m") == month_input]
        if not filtered:
            messagebox.showinfo("No Data", f"No expenses found for {month_input}.")
            return

        category_totals = defaultdict(float)
        for exp in filtered:
            category_totals[exp["category"]] += exp["amount"]

        categories = list(category_totals.keys())
        amounts = list(category_totals.values())

        # Ask user for chart type
        chart_type = simpledialog.askstring("Chart Type", "Enter chart type (pie/bar):", parent=self)
        if not chart_type:
            return
        chart_type = chart_type.lower()
        plt.figure(figsize=(8,6))
        if chart_type == "pie":
            plt.pie(amounts, labels=categories, autopct='%1.1f%%', startangle=140)
            plt.title(f"Expenses by Category for {month_input}")
        elif chart_type == "bar":
            plt.bar(categories, amounts, color='skyblue')
            plt.title(f"Expenses by Category for {month_input}")
            plt.ylabel("Amount (₹)")
            plt.xticks(rotation=45, ha='right')
        else:
            messagebox.showerror("Invalid Input", "Chart type must be 'pie' or 'bar'.")
            return
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    app = ExpenseTrackerApp()
    app.mainloop()
