import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
import re
from datetime import datetime
import csv

add_on = True

# Connect to the SQLite database
con = sqlite3.connect('finance_records.db')

# Create a cursor object to execute SQL queries
cursor = con.cursor()
print("Connected to the database successfully!")

income_categories = ["Salary", "Bonus", "Savings", "Other"]
expense_categories = ["Food", "Rent", "Social Life", "Pets", "Transports", "Household", "Apparel", "Beauty", "Health", "Education", "Other"]

# Get categories
def get_categories():
    while True:
        record_type = input("Do you want to add it to income(i) or expense(e)?\n==> ").lower()
        if record_type == 'i' or record_type == 'income':
            print("\n-----------------------------------")
            print("|", " | ".join(income_categories), "|")
            print("-----------------------------------\n")
            print("Please select one of options above.")
            category_option = input("==> ").title()
        elif record_type == 'e' or record_type == 'expense':
            print("\n------------------------------------------------------------")
            print("|", " | ".join(expense_categories[0:5]), "            |")
            print("|", " | ".join(expense_categories[5:11]), "|")
            print("------------------------------------------------------------\n")
            print("Please select one of options above.")
            category_option = input("==> ").title()
            return category_option
        else:
            print("Please enter valid value!")
        if category_option not in expense_categories and category_option not in income_categories:
            print("Please enter one of the options.")
            continue
        

# Get value of amount (positive/negative)
def get_amount(category):
    value = float(input("Amount: "))
    if category in income_categories:
        return value
    elif category in expense_categories:
        return -value
    
# Get date
def get_date():
        date = input("Date (YYYY-MM-DD): ")
        check_date = r'^\d{4}-\d{2}-\d{2}$'
        while True:
            if re.match(check_date, date):
                return date
            else:
                print("Date would be YYYY-MM-DD. Please try again.")
                date = input("Date (YYYY-MM-DD): ")
                continue
        
# Add features
def add_records():
    date = get_date()
    category = get_categories()
    amount = get_amount(category)
    description = input("Description: ")
    record_query = """
    INSERT INTO finance_records (date, amount, category, description) 
    VALUES (?, ?, ?, ?);
"""
    record = (date, amount, category, description)
    cursor.execute(record_query, record)
    con.commit()

# View records
def view_records():
    select_query = "SELECT * FROM finance_records;"
    cursor.execute(select_query)
    records = cursor.fetchall()
    print("Trans.")
    for record in records:
        print(record)
    if not record:
        print("No data in the database.")
    with open('Financial_records.csv', 'w', newline='') as csvfile:
        fieldnames = ['id', 'date', 'amount', 'category', 'summary']
        write = csv.writer(csvfile)
        write.writerow(fieldnames)
        write.writerows(records)

# Summarize data; calculate total income, total expenses, and net balance
def summarize_data():
    datas = []
    income_query = "SELECT SUM(amount) FROM finance_records WHERE amount > 0"
    expense_query = "SELECT SUM(amount) FROM finance_records WHERE amount < 0"
    net_balance_query = "SELECT SUM(amount) FROM finance_records"
    query_lists = [income_query, expense_query, net_balance_query]
    for qeury_list in query_lists:
        cursor.execute(qeury_list)
        records = cursor.fetchone()
        datas.append(records)
    print("======== Summmary ========")
    print(f"Total income: {datas[0]}\nTotal expenses: {datas[1]}\nNet balance: {datas[2]}")
    print("==========================")
    
    

# Filter records by data range, category, and type (income/expense)
def filter_records():
    try:
        option = int(input("How'd you filter records?\n1. Date\n2. Category\n3. type(income/expense)\n==> "))
        if option == 1:
            cursor.execute("SELECT * FROM finance_records ORDER BY date")
        elif option == 2:
            print("\n-----------------------------------------------------------")
            print("|", " | ".join(income_categories), "|")
            print("|", " | ".join(expense_categories[0:5]), "            |")
            print("|", " | ".join(expense_categories[5:11]), "|")
            print("------------------------------------------------------------\n")
            filter_category = input("Select a category\n==> ").title()
            cursor.execute("SELECT * FROM finance_records WHERE category=?",(filter_category, ))
            if filter_category not in income_categories and filter_category not in expense_categories:
                print("Invalid value! Please try again.")
        elif option == 3:
            type_option = input("Select a type; income(i) or expense(e)\n==> ").lower()
            if type_option == 'i':
                filter_query = "SELECT * FROM finance_records WHERE amount > 0"
            elif type_option == 'e':
                filter_query = "SELECT * FROM finance_records WHERE amount < 0"
            else:
                print("please try again.")
            cursor.execute(filter_query)
        records = cursor.fetchall()
        for record in records:
            print(record)
        if not record:
            print("No data in the database")
    except ValueError:
        print("Invalid value! Please enter a number.")
    except UnboundLocalError:
        print("There is no matching items.")

def view_summary_charts():
    try:
        option = int(input("What chart would you like to view?\n1. Categories and total spending\n2. Expenses over time\n3. Income over time\n4. Compare total income and expenses\n==> "))
        now = datetime.now()
        if option == 1:
            total_query = "SELECT category, SUM(amount) FROM finance_records GROUP BY category"
            cursor.execute(total_query)
            records = cursor.fetchall()
            for record in records:
                plt.bar(record[0], record[1])
                plt.text(record[0], 0, record[1], ha='center')
            plt.title("total spending over category")
            plt.xlabel("category")
            plt.ylabel("SUM")
            filename = "total_spending_over_time"

        elif option == 2:
            expense_query = "SELECT date, SUM(amount) FROM finance_records WHERE amount < 0 GROUP BY date ORDER BY date"
            cursor.execute(expense_query)
            records = cursor.fetchall()
            x_val = [record[0] for record in records]
            y_val = [-record[1] for record in records]
            
            plt.plot(x_val, y_val, color="red")
            plt.title("Expenses over time")
            plt.xlabel("Date")
            plt.ylabel("Expenses")
            plt.legend(["expense"])
            filename = "expenses_over_time"

        elif option == 3:
            income_query = "SELECT date, SUM(amount) FROM finance_records WHERE amount > 0 GROUP BY date ORDER BY date"
            cursor.execute(income_query)
            records = cursor.fetchall()
            x_val = [record[0] for record in records]
            y_val = [record[1] for record in records]
            
            plt.plot(x_val, y_val)
            plt.title("Income over time")
            plt.xlabel("Date")
            plt.ylabel("Income")
            plt.legend(["income"])
            filename = "income_over_time"

        elif option == 4:
            total_dict = {}
            income_query = "SELECT SUM(amount) FROM finance_records WHERE amount > 0"
            expense_query = "SELECT SUM(amount) FROM finance_records WHERE amount < 0"
            cursor.execute(income_query)
            income_records = cursor.fetchall()
            total_dict["Total_income"] = [record[0] for record in income_records]
            cursor.execute(expense_query)
            expense_records = cursor.fetchall()
            total_dict["Total_expenses"] = [-record[0] for record in expense_records]

            sns.set_style("darkgrid")            
            ax = sns.barplot(data=total_dict,width=0.5,palette="pastel",legend=True)
            ax.set_title("Total income vs. Total expenses")
            ax.bar_label(ax.containers[0])
            ax.bar_label(ax.containers[1])

            filename = "total_income_vs_total_expenses"
            
        plt.show()
        plt.savefig(f"{filename}_{now.strftime("%Y-%m-%d")}.png")

    except ValueError:
        print("Invalid value! Please enter a number.")
    except UnboundLocalError:
        print("There is no matching items.")
    return

while add_on:
    print("\n================================")
    print("| Welcome! How can I help you? |")
    print("================================\n")
    try:
        option = int(input("1. Add records\n2. View records\n3. Summary\n4. Sort records\n5. View Summary Charts\n6. Exit\n==> "))
        if option == 1:
            print("Add your financial records.")
            add_records()
            view_records()
        elif option == 2:
            print("View your whole records and save them as csv file.")
            view_records()
        elif option == 3:
            print("Provide the summary of your all records")
            summarize_data()
        elif option == 4:
            print("Filter records depending on your choice.")
            filter_records()
        elif option == 5:
            print("View summary charts depending on your choice.")
            view_summary_charts()
        elif option == 6:
            print("\n=========================")
            print("|  Thank you for using  |")
            print("=========================\n")
            add_on = False
        else:
            print("Invalid value! Please try again!")
    except ValueError:
        print("Value Error: Invalid value! Please try again!")

con.close()
print("Database connection closed!")