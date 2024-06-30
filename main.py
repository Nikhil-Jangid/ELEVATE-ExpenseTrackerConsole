from datetime import datetime, timedelta
from file_handler import FileHandler

class ExpenseTracker:
    def __init__(self):
        self.exp = FileHandler.load_expenses()
        self.rec_exp = FileHandler.load_recurring_expenses()
        self.apply_rec_exp()

    def add_exp(self):
        cat = input("Enter the category: ").strip()
        amt = self.get_valid_amt()
        date = self.get_date()
        self.store_exp(cat, amt, date)
        FileHandler.save_expense(cat, amt, date)
        self.add_rec_exp_prompt(cat, amt, date)

    def get_valid_amt(self):
        while True:
            try:
                amt = float(input("Enter the amount: "))
                if amt < 0:
                    raise ValueError("Amount cannot be negative.")
                return amt
            except ValueError as e:
                print(f"Invalid input: {e}. Please enter a valid number.")

    def get_date(self):
        date = input("Enter the date (YYYY-MM-DD) or leave empty for today: ").strip()
        return date or datetime.today().strftime('%Y-%m-%d')

    def store_exp(self, cat, amt, date):
        self.exp.setdefault(cat, []).append((amt, date))

    def add_rec_exp_prompt(self, cat, amt, date):
        recur = input("Is this a recurring expense? (yes/no): ").strip().lower()
        if recur == 'yes':
            freq = input("Enter the frequency (daily, weekly, monthly): ").strip().lower()
            self.rec_exp.append((cat, amt, freq, date))
            FileHandler.save_recurring_expenses(self.rec_exp)

    def calc_total_exp(self):
        return sum(amt for amts in self.exp.values() for amt, _ in amts)

    def show_summary(self):
        print("\nExpense Summary by Category:")
        for cat, amts in self.exp.items():
            total = sum(amt for amt, _ in amts)
            print(f"{cat}: {total:.2f}/-")

        print(f"\nTotal Expenses: {self.calc_total_exp():.2f}")

    def show_monthly_summary(self):
        month_exp = {}
        for amts in self.exp.values():
            for amt, date in amts:
                month = date[:7]
                month_exp[month] = month_exp.get(month, 0) + amt

        print("\nMonthly Expense Summary:")
        for month, total in month_exp.items():
            print(f"{month}: ${total:.2f}")

    def edit_exp(self):
        self.show_summary()
        cat = input("Enter the category to edit: ").strip()
        if cat in self.exp:
            self.print_exp(cat)
            idx = int(input("Enter the number to edit: ")) - 1
            if 0 <= idx < len(self.exp[cat]):
                new_amt = self.get_valid_amt()
                new_date = self.get_date()
                self.exp[cat][idx] = (new_amt, new_date)
                FileHandler.save_all_expenses(self.exp)
                print("Expense updated successfully.")
            else:
                print("Invalid selection.")
        else:
            print("Category not found.")

    def del_exp(self):
        self.show_summary()
        cat = input("Enter the category to delete: ").strip()
        if cat in self.exp:
            self.print_exp(cat)
            idx = int(input("Enter the number to delete: ")) - 1
            if 0 <= idx < len(self.exp[cat]):
                del self.exp[cat][idx]
                if not self.exp[cat]:
                    del self.exp[cat]
                FileHandler.save_all_expenses(self.exp)
                print("Expense deleted successfully.")
            else:
                print("Invalid selection.")
        else:
            print("Category not found.")

    def print_exp(self, cat):
        for i, (amt, date) in enumerate(self.exp[cat]):
            print(f"{i+1}. Amount: {amt}, Date: {date}")

    def search_exp(self):
        choice = input("Search by category or date range? (category/date): ").strip().lower()
        if choice == 'category':
            self.search_by_cat()
        elif choice == 'date':
            self.search_by_date()
        else:
            print("Invalid choice.")

    def search_by_cat(self):
        cat = input("Enter the category to search for: ").strip()
        if cat in self.exp:
            print(f"Expenses in category {cat}:")
            self.print_exp(cat)
        else:
            print("Category not found.")

    def search_by_date(self):
        start_date = input("Enter the start date (YYYY-MM-DD): ").strip()
        end_date = input("Enter the end date (YYYY-MM-DD): ").strip()
        print(f"Expenses from {start_date} to {end_date}:")
        for cat, amts in self.exp.items():
            for amt, date in amts:
                if start_date <= date <= end_date:
                    print(f"Category: {cat}, Amount: {amt}, Date: {date}")

    def apply_rec_exp(self):
        for cat, amt, freq, start_date in self.rec_exp:
            last_date = datetime.strptime(start_date, '%Y-%m-%d')
            today = datetime.today()
            while last_date < today:
                if freq == 'daily':
                    last_date += timedelta(days=1)
                elif freq == 'weekly':
                    last_date += timedelta(weeks=1)
                elif freq == 'monthly':
                    last_date += timedelta(weeks=4)
                if last_date <= today:
                    self.store_exp(cat, amt, last_date.strftime('%Y-%m-%d'))
                    FileHandler.save_expense(cat, amt, last_date.strftime('%Y-%m-%d'))

    def main(self):
        while True:
            print("\nExpense Tracker")
            print("1. Add an Expense")
            print("2. Display Summary")
            print("3. Display Monthly Summary")
            print("4. Edit an Expense")
            print("5. Delete an Expense")
            print("6. Search Expenses")
            print("7. Exit")
            choice = input("Enter your choice (1/2/3/4/5/6/7): ").strip()

            if choice == '1':
                self.add_exp()
            elif choice == '2':
                self.show_summary()
            elif choice == '3':
                self.show_monthly_summary()
            elif choice == '4':
                self.edit_exp()
            elif choice == '5':
                self.del_exp()
            elif choice == '6':
                self.search_exp()
            elif choice == '7':
                print("Exiting Expense Tracker. Goodbye!")
                break
            else:
                print("Invalid choice. Please enter 1, 2, 3, 4, 5, 6, or 7.")

if __name__ == "__main__":
    ExpenseTracker().main()
