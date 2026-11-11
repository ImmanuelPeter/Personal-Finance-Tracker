import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import sqlite3
from datetime import datetime
import matplotlib.pyplot as plt

class FinanceTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Personal Finance Tracker")
        self.root.geometry("1000x700")
        self.root.configure(bg="#f0f0f0")

        # Create database
        self.create_database()

        # Create main frames
        self.create_frames()

        # Initialize variables
        self.selected_item = None
        self.load_transactions()
        self.calculate_savings()

    def create_database(self):
        self.conn = sqlite3.connect('finance_tracker.db')
        self.cursor = self.conn.cursor()
        # Create table if it does not exist
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY,
                date TEXT NOT NULL,
                description TEXT NOT NULL,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                priority TEXT NOT NULL,
                type TEXT NOT NULL,
                currency TEXT NOT NULL
            )
        ''')
        self.conn.commit()

    def create_frames(self):
        # Title Label
        title_label = tk.Label(self.root, text="Personal Finance Tracker",
                                font=('Helvetica', 16, 'bold'), bg="#f0f0f0")
        title_label.pack(pady=10)

        # Input Frame
        input_frame = tk.LabelFrame(self.root, text="Transaction Details",
                                     bg="#e0e0e0", font=('Helvetica', 10, 'bold'))
        input_frame.pack(pady=10, padx=10, fill="x")

        # Date
        tk.Label(input_frame, text="Date:", bg="#e0e0e0").grid(row=0, column=0, padx=5, pady=5)
        self.date_entry = DateEntry(input_frame, width=12, background='darkblue',
                                     foreground='white', borderwidth=2)
        self.date_entry.set_date(datetime.now())
        self.date_entry.grid(row=0, column=1, padx=5, pady=5)

        # Description
        tk.Label(input_frame, text="Description:", bg="#e0e0e0").grid(row=0, column=2, padx=5, pady=5)
        self.desc_entry = tk.Entry(input_frame, width=30)
        self.desc_entry.grid(row=0, column=3, padx=5, pady=5)

        # Amount
        tk.Label(input_frame, text="Amount:", bg="#e0e0e0").grid(row=1, column=0, padx=5, pady=5)
        self.amount_entry = tk.Entry(input_frame)
        self.amount_entry.grid(row=1, column=1, padx=5, pady=5)

        # Category
        tk.Label(input_frame, text="Category:", bg="#e0e0e0").grid(row=1, column=2, padx=5, pady=5)
        categories = ["Food", "Transport", "Utilities", "Entertainment", "Shopping", "Rent", "Salary", "Other"]
        self.category_var = tk.StringVar()
        self.category_combo = ttk.Combobox(input_frame, textvariable=self.category_var,
                                            values=categories, width=27)
        self.category_combo.grid(row=1, column=3, padx=5, pady=5)

        # Priority
        tk.Label(input_frame, text="Priority:", bg="#e0e0e0").grid(row=2, column=0, padx=5, pady=5)
        priorities = ["High", "Medium", "Low"]
        self.priority_var = tk.StringVar()
        self.priority_combo = ttk.Combobox(input_frame, textvariable=self.priority_var,
                                            values=priorities)
        self.priority_combo.grid(row=2, column=1, padx=5, pady=5)

        # Type
        tk.Label(input_frame, text="Type:", bg="#e0e0e0").grid(row=2, column=2, padx=5, pady=5)
        types = ["Income", "Expense"]
        self.type_var = tk.StringVar()
        self.type_combo = ttk.Combobox(input_frame, textvariable=self.type_var,
                                        values=types)
        self.type_combo.grid(row=2, column=3, padx=5, pady=5)

        # Currency
        tk.Label(input_frame, text="Currency:", bg="#e0e0e0").grid(row=3, column=0, padx=5, pady=5)
        self.currency_var = tk.StringVar(value="USD")  # Default currency
        currencies = ["USD", "EUR", "GBP", "INR", "MWK"]
        self.currency_combo = ttk.Combobox(input_frame, textvariable=self.currency_var,
                                            values=currencies)
        self.currency_combo.grid(row=3, column=1, padx=5, pady=5)

        # Buttons Frame
        button_frame = tk.Frame(self.root, bg="#e0e0e0")
        button_frame.pack(pady=5, padx=10, fill="x")

        # Add Button
        tk.Button(button_frame, text="Add Transaction", command=self.add_transaction,
                  bg="#4CAF50", fg="white", width=15, font=('Helvetica', 9, 'bold')).pack(side=tk.LEFT, padx=5)

        # Update Button
        tk.Button(button_frame, text="Update", command=self.update_transaction,
                  bg="#2196F3", fg="white", width=15, font=('Helvetica', 9, 'bold')).pack(side=tk.LEFT, padx=5)

        # Delete Button
        tk.Button(button_frame, text="Delete", command=self.delete_transaction,
                  bg="#f44336", fg="white", width=15, font=('Helvetica', 9, 'bold')).pack(side=tk.LEFT, padx=5)

        # Clear Button
        tk.Button(button_frame, text="Clear", command=self.clear_entries,
                  bg="#607d8b", fg="white", width=15, font=('Helvetica', 9, 'bold')).pack(side=tk.LEFT, padx=5)

        # Savings Frame
        savings_frame = tk.LabelFrame(self.root, text="Savings", bg="#e0e0e0",
                                      font=('Helvetica', 10, 'bold'))
        savings_frame.pack(pady=5, padx=10, fill="x")

        self.income_label = tk.Label(savings_frame, text="Total Income: $0.00", bg="#e0e0e0")
        self.income_label.pack(pady=5)

        self.expense_label = tk.Label(savings_frame, text="Total Expenses: $0.00", bg="#e0e0e0")
        self.expense_label.pack(pady=5)

        self.savings_label = tk.Label(savings_frame, text="Total Savings: $0.00", bg="#e0e0e0")
        self.savings_label.pack(pady=5)

        # Reports and Stats Buttons
        tk.Button(button_frame, text="Generate Report", command=self.generate_report,
                  bg="#9C27B0", fg="white", width=15, font=('Helvetica', 9, 'bold')).pack(side=tk.RIGHT, padx=5)

        # Stats Button
        tk.Button(button_frame, text="Show Statistics", command=self.show_statistics,
                  bg="#FF9800", fg="white", width=15, font=('Helvetica', 9, 'bold')).pack(side=tk.RIGHT, padx=5)

        # Search Frame
        search_frame = tk.LabelFrame(self.root, text="Search", bg="#e0e0e0",
                                     font=('Helvetica', 10, 'bold'))
        search_frame.pack(pady=5, padx=10, fill="x")

        tk.Label(search_frame, text="Search Term:", bg="#e0e0e0").pack(side=tk.LEFT, padx=5)
        self.search_entry = tk.Entry(search_frame, width=40)
        self.search_entry.pack(side=tk.LEFT, padx=5)

        tk.Button(search_frame, text="Search", command=self.search_transactions,
                  bg="#FF9800", fg="white", width=10, font=('Helvetica', 9, 'bold')).pack(side=tk.LEFT, padx=5)

        tk.Button(search_frame, text="Show All", command=self.load_transactions,
                  bg="#9C27B0", fg="white", width=10, font=('Helvetica', 9, 'bold')).pack(side=tk.LEFT, padx=5)

        # Transactions Frame
        transactions_frame = tk.LabelFrame(self.root, text="Transactions",
                                           bg="#e0e0e0", font=('Helvetica', 10, 'bold'))
        transactions_frame.pack(pady=5, padx=10, fill="both", expand=True)

        # Treeview
        self.tree = ttk.Treeview(transactions_frame,
                                  columns=("ID", "Date", "Description", "Amount", "Category", "Priority", "Type", "Currency"),
                                  show="headings", height=15)

        # Define headings
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)

        # Define columns
        self.tree.column("ID", width=50)
        self.tree.column("Date", width=100)
        self.tree.column("Description", width=300)
        self.tree.column("Amount", width=100)
        self.tree.column("Category", width=100)
        self.tree.column("Priority", width=100)
        self.tree.column("Type", width=100)
        self.tree.column("Currency", width=100)

        # Add scrollbar
        scrollbar = ttk.Scrollbar(transactions_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Pack tree and scrollbar
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Bind select event
        self.tree.bind('<<TreeviewSelect>>', self.item_selected)

    def add_transaction(self):
        date = self.date_entry.get()
        description = self.desc_entry.get()
        amount = self.amount_entry.get()
        category = self.category_var.get()
        priority = self.priority_var.get()
        transaction_type = self.type_var.get()
        currency = self.currency_var.get()

        if not all([date, description, amount, category, priority, transaction_type, currency]):
            messagebox.showerror("Error", "Please fill all fields")
            return

        try:
            amount = float(amount)
        except ValueError:
            messagebox.showerror("Error", "Amount must be a number")
            return

        try:
            self.cursor.execute('''
                INSERT INTO transactions (date, description, amount, category, priority, type, currency)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (date, description, amount, category, priority, transaction_type, currency))
            self.conn.commit()
            self.clear_entries()
            self.load_transactions()
            self.calculate_savings()
            messagebox.showinfo("Success", "Transaction added successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def update_transaction(self):
        if not self.selected_item:
            messagebox.showerror("Error", "Please select a transaction to update")
            return

        date = self.date_entry.get()
        description = self.desc_entry.get()
        amount = self.amount_entry.get()
        category = self.category_var.get()
        priority = self.priority_var.get()
        transaction_type = self.type_var.get()
        currency = self.currency_var.get()

        if not all([date, description, amount, category, priority, transaction_type, currency]):
            messagebox.showerror("Error", "Please fill all fields")
            return

        try:
            amount = float(amount)
        except ValueError:
            messagebox.showerror("Error", "Amount must be a number")
            return

        try:
            self.cursor.execute('''
                UPDATE transactions
                SET date=?, description=?, amount=?, category=?, priority=?, type=?, currency=?
                WHERE id=?
            ''', (date, description, amount, category, priority, transaction_type, currency, self.selected_item))
            self.conn.commit()
            self.clear_entries()
            self.load_transactions()
            self.calculate_savings()
            self.selected_item = None
            messagebox.showinfo("Success", "Transaction updated successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def delete_transaction(self):
        if not self.selected_item:
            messagebox.showerror("Error", "Please select a transaction to delete")
            return

        if messagebox.askyesno("Confirm", "Are you sure you want to delete this transaction?"):
            try:
                self.cursor.execute("DELETE FROM transactions WHERE id=?", (self.selected_item,))
                self.conn.commit()
                self.clear_entries()
                self.load_transactions()
                self.calculate_savings()
                self.selected_item = None
                messagebox.showinfo("Success", "Transaction deleted successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def search_transactions(self):
        search_term = self.search_entry.get()

        if not search_term:
            self.load_transactions()
            return

        for item in self.tree.get_children():
            self.tree.delete(item)

        self.cursor.execute('''
            SELECT * FROM transactions
            WHERE description LIKE ? OR category LIKE ? OR priority LIKE ? OR type LIKE ?
        ''', (f'%{search_term}%', f'%{search_term}%', f'%{search_term}%', f'%{search_term}%'))

        for row in self.cursor.fetchall():
            self.tree.insert("", "end", values=row)

    def load_transactions(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        self.cursor.execute("SELECT * FROM transactions ORDER BY date DESC")
        for row in self.cursor.fetchall():
            self.tree.insert("", "end", values=row)

    def item_selected(self, event):
        selected_items = self.tree.selection()
        if selected_items:
            item = self.tree.item(selected_items[0])
            values = item['values']
            self.selected_item = values[0]

            # Fill entries with selected data
            self.date_entry.set_date(values[1])
            self.desc_entry.delete(0, tk.END)
            self.desc_entry.insert(0, values[2])
            self.amount_entry.delete(0, tk.END)
            self.amount_entry.insert(0, values[3])
            self.category_var.set(values[4])
            self.priority_var.set(values[5])
            self.type_var.set(values[6])
            self.currency_var.set(values[7])

    def clear_entries(self):
        self.date_entry.set_date(datetime.now())
        self.desc_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)
        self.category_var.set("")
        self.priority_var.set("")
        self.type_var.set("")
        self.currency_var.set("USD")
        self.search_entry.delete(0, tk.END)

    def calculate_savings(self):
        total_income = 0.0
        total_expense = 0.0

        self.cursor.execute("SELECT SUM(amount) FROM transactions WHERE type='Income'")
        income = self.cursor.fetchone()[0]
        total_income = income if income else 0.0
        self.income_label.config(text=f"Total Income: ${total_income:.2f}")

        self.cursor.execute("SELECT SUM(amount) FROM transactions WHERE type='Expense'")
        expense = self.cursor.fetchone()[0]
        total_expense = expense if expense else 0.0
        self.expense_label.config(text=f"Total Expenses: ${total_expense:.2f}")

        savings = total_income - total_expense
        self.savings_label.config(text=f"Total Savings: ${savings:.2f}")

    def generate_report(self):
        self.cursor.execute('''
            SELECT category, SUM(amount) FROM transactions
            WHERE type='Expense'
            GROUP BY category
        ''')

        expense_report = self.cursor.fetchall()
        
        if not expense_report:
            messagebox.showinfo("Report", "No expense data available.")
            return

        report_message = "Expense Report by Category:\n\n"
        for category, total in expense_report:
            report_message += f"{category}: ${total:.2f}\n"

        self.cursor.execute('''
            SELECT category, SUM(amount) FROM transactions
            WHERE type='Income'
            GROUP BY category
        ''')
        
        income_report = self.cursor.fetchall()
        
        report_message += "\nIncome Report by Category:\n\n"
        for category, total in income_report:
            report_message += f"{category}: ${total:.2f}\n"

        self.cursor.execute('''
            SELECT SUM(amount) FROM transactions WHERE type='Expense'
        ''')
        total_expenses = self.cursor.fetchone()[0] or 0.0

        self.cursor.execute('''
            SELECT SUM(amount) FROM transactions WHERE type='Income'
        ''')
        total_income = self.cursor.fetchone()[0] or 0.0

        total_savings = total_income - total_expenses
        report_message += f"\nTotal Income: ${total_income:.2f}\n"
        report_message += f"Total Expenses: ${total_expenses:.2f}\n"
        report_message += f"Total Savings: ${total_savings:.2f}\n"

        messagebox.showinfo("Financial Report", report_message)

    def show_statistics(self):
        # Fetch Expenses statistics
        self.cursor.execute('''
            SELECT category, SUM(amount) FROM transactions
            WHERE type='Expense'
            GROUP BY category
        ''')
        expense_data = self.cursor.fetchall()

        if not expense_data:
            messagebox.showinfo("Statistics", "No expense data available.")
            return
        
        expense_labels = [item[0] for item in expense_data]
        expense_sizes = [item[1] for item in expense_data]

        # Fetch Income statistics
        self.cursor.execute('''
            SELECT category, SUM(amount) FROM transactions
            WHERE type='Income'
            GROUP BY category
        ''')
        income_data = self.cursor.fetchall()

        if not income_data:
            messagebox.showinfo("Statistics", "No income data available.")
            return

        income_labels = [item[0] for item in income_data]
        income_sizes = [item[1] for item in income_data]

        # Creating a figure with subplots
        fig, axs = plt.subplots(2, 2, figsize=(12, 10))

        # Bar Chart for Expenses
        axs[0, 0].bar(expense_labels, expense_sizes, color='skyblue')
        axs[0, 0].set_title("Expenses by Category")
        axs[0, 0].set_xlabel("Category")
        axs[0, 0].set_ylabel("Amount ($)")
        axs[0, 0].tick_params(axis='x', rotation=45)  # Rotate x-axis labels

        # Pie Chart for Expenses
        axs[0, 1].pie(expense_sizes, labels=expense_labels, autopct='%1.1f%%', startangle=90)
        axs[0, 1].set_title("Expenses Distribution")

        # Bar Chart for Income
        axs[1, 0].bar(income_labels, income_sizes, color='lightgreen')
        axs[1, 0].set_title("Income by Category")
        axs[1, 0].set_xlabel("Category")
        axs[1, 0].set_ylabel("Amount ($)")
        axs[1, 0].tick_params(axis='x', rotation=45)  # Rotate x-axis labels

        # Pie Chart for Income
        axs[1, 1].pie(income_sizes, labels=income_labels, autopct='%1.1f%%', startangle=90)
        axs[1, 1].set_title("Income Distribution")

        plt.tight_layout()  # Adjust layout
        plt.show()

def main():
    root = tk.Tk()
    app = FinanceTracker(root)
    root.mainloop()

if __name__ == "__main__":
    main()