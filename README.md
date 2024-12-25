# personal_financial_tracker

# Description

# To track of a user's finance record personally, the user can add and view income or expense records, with date, amount, category, and description. The user is able to filter records by data range, category, and type(income or expense) and summarize data by calculating total income, total expenses, and net balance. This code is made up of Python, SQLite, and Python libraries, and will show up visualization options (summary charts) by using importing libraries; matplotlib.pyplot and seaborn.

# How does it work

# Once a user runs this code, the program will show up six options with welcome sign, which are add records, view records, summary of total expenses, income, and net balance, sort records by date, category, and type(income or expense), view summary charts through bar graph and line graph. The difference between summary and summary charts is summary charts provide information as graphs. 'View summary charts' allows the user to check categories and total spending, expenses over time, income over time and compare total income and expenses. The user is able to save the image of charts in their folder. 

# Python version, required libraries, and database setup
Python 3.13.0

Required libraries: 
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
import re
from datetime import datetime
import csv

database setup:
CREATE TABLE IF NOT EXISTS finance_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date DATE NOT NULL,
    amount FLOAT NOT NULL,
    category STRING NOT NULL,
    description TEXT
);


# Improvement

-> Get date: To avoid users typo, add def get_data by using r'^\d{4}-\d{2}-\d{2}$' and check the input from users through re.match(check_date, date). If it matches, return it. If not users need to type the date again until it matches.

-> Get category: Users require to type one of the category options. If the input isn't in the categories or typo, users should go back to input.

-> Visualization: Show up title, axis labels, and legends to all plots for clarity.

-> Data export: Allow users to export records as a CSV file for external use by def view_records. Once users view records, records would save and update in a CSV file (called 'Financial_records.csv') automatically.
