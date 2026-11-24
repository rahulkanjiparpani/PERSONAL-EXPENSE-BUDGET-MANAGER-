import pandas as pd
from datetime import datetime

# Personal Expense and Budget Manager - Project No. 46
FILENAME = 'expenses.csv'

# Ensure the CSV file exists with headers if it doesn't already
try:
    pd.read_csv(FILENAME)
except FileNotFoundError:
    df_init = pd.DataFrame(columns=['Date', 'Category', 'Amount'])
    df_init.to_csv(FILENAME, index=False)

budget = 0.0

def validate_date(date_str):
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False

while True:
    print("\n========= Personal Expense and Budget Manager (Beta version) =========")
    print("1. Set budget")
    print("2. Add expense")
    print("3. Category summary")
    print("4. Report")
    print("5. Exit")
    
    choice = input("Enter your choice: ")
    
    if choice == '1':
        try:
            budget = float(input("Enter your monthly budget: "))
            print(f"Monthly budget set: {int(budget) if budget.is_integer() else budget}")
        except ValueError:
            print("Invalid budget amount. Please enter a number.")
            
    elif choice == '2':
        date = input("Enter date (YYYY-MM-DD): ")
        if not validate_date(date):
            print("Invalid date. Use YYYY-MM-DD.")
            continue
            
        category = input("Enter category: ").strip()
        
        try:
            amount = float(input("Enter amount: "))
            if amount <= 0:
                print("Invalid amount. Amount must be a positive number. Expense not saved.")
                continue
        except ValueError:
            print("Invalid amount. Please enter a valid number.")
            continue
            
        # Append expense to CSV using pandas
        new_row = pd.DataFrame([[date, category, amount]], columns=['Date', 'Category', 'Amount'])
        new_row.to_csv(FILENAME, mode='a', header=False, index=False)
        print("Expense saved.")
        
        # Calculate total spent
        df = pd.read_csv(FILENAME)
        total_spent = df['Amount'].sum()
        remaining = budget - total_spent
        
        print(f"Total spent: {int(total_spent) if total_spent.is_integer() else total_spent} │ Remaining: {int(remaining) if remaining.is_integer() else remaining}")
        
        if budget > 0:
            if total_spent > budget:
                print("Budget exceeded!")
            elif total_spent == budget:
                percent = (total_spent / budget) * 100
                print(f"Budget fully used ({percent:.2f}%).")
            elif total_spent >= 0.8 * budget:
                percent = (total_spent / budget) * 100
                print(f"Warning: {percent:.2f}% of the budget used.")
                
    elif choice == '3':
        try:
            df = pd.read_csv(FILENAME)
            if df.empty:
                print("No expenses recorded yet.")
            else:
                summary = df.groupby('Category')['Amount'].sum()
                print("Category Summary:")
                for cat, amt in summary.items():
                    print(f"{cat}: {amt}")
        except Exception:
            print("Error reading expenses file.")
            
    elif choice == '4':
        try:
            if budget == 0:
                print("ERROR 404:-Budget not found")
                continue
                
            df = pd.read_csv(FILENAME)
            total_spent = df['Amount'].sum() if not df.empty else 0
            remaining_budget = budget - total_spent
            
            print("Total spent:", total_spent)
            print("Remaining budget:", remaining_budget)
            
            if not df.empty:
                summary = df.groupby('Category')['Amount'].sum()
                print("Category Summary:")
                for cat, amt in summary.items():
                    print(f"{cat}: {amt}")
            
            if total_spent > budget:
                print("Budget exceeded!")
            elif total_spent == budget:
                percent = (total_spent / budget) * 100
                print(f"Budget fully used ({percent:.2f}%).")
            elif total_spent >= 0.8 * budget:
                percent_more = (total_spent / budget) * 100
                print(f"Warning: {percent_more:.2f}% of the budget used.")
                
        except NameError:
            print("ERROR 404:-Budget not found")
        except Exception:
            print("something went wrong")
            
    elif choice == '5':
        print("Exiting...")
        break
    else:
        print("Invalid choice. Please select from 1 to 5.")