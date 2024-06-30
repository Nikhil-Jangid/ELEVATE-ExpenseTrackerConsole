import csv
import os

class FileHandler:
    @staticmethod
    def get_expenses_path():
        return os.path.join(os.path.dirname(__file__), 'expenses.csv')

    @staticmethod
    def get_recurring_expenses_path():
        return os.path.join(os.path.dirname(__file__), 'recurring_expenses.csv')

    @staticmethod
    def save_expense(cat, amt, date):
        file_path = FileHandler.get_expenses_path()
        file_exists = os.path.isfile(file_path)
        with open(file_path, mode='a', newline='') as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(['Category', 'Amount', 'Date'])
            writer.writerow([cat, amt, date])

    @staticmethod
    def load_expenses():
        exp = {}
        file_path = FileHandler.get_expenses_path()
        if os.path.isfile(file_path):
            with open(file_path, mode='r') as file:
                reader = csv.reader(file)
                next(reader)
                for row in reader:
                    cat, amt, date = row
                    amt = float(amt)
                    exp.setdefault(cat, []).append((amt, date))
        return exp

    @staticmethod
    def save_all_expenses(exp):
        file_path = FileHandler.get_expenses_path()
        with open(file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Category', 'Amount', 'Date'])
            for cat, amts in exp.items():
                for amt, date in amts:
                    writer.writerow([cat, amt, date])

    @staticmethod
    def save_recurring_expenses(rec_exp):
        file_path = FileHandler.get_recurring_expenses_path()
        with open(file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Category', 'Amount', 'Frequency', 'Start Date'])
            for cat, amt, freq, start_date in rec_exp:
                writer.writerow([cat, amt, freq, start_date])

    @staticmethod
    def load_recurring_expenses():
        rec_exp = []
        file_path = FileHandler.get_recurring_expenses_path()
        if os.path.isfile(file_path):
            with open(file_path, mode='r') as file:
                reader = csv.reader(file)
                next(reader)
                for row in reader:
                    cat, amt, freq, start_date = row
                    amt = float(amt)
                    rec_exp.append((cat, amt, freq, start_date))
        return rec_exp
