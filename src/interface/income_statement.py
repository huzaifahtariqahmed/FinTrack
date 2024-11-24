# Importing essential modules
from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QHeaderView
import sys
import pyodbc

# FOR GENERATING A CONNECTION STRING
server = 'DESKTOP-6M55HJA\\SQLSERVER1'
database = 'Northwind'  # Name of your Northwind database
use_windows_authentication = True  # Set to True to use Windows Authentication
username = 'your_username'  # Specify a username if not using Windows Authentication
password = 'your_password'  # Specify a password if not using Windows Authentication


# Create the connection string based on the authentication method chosen
if use_windows_authentication:
    connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
else:
    connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'



class IncomeStatement(QtWidgets.QMainWindow):
    def __init__(self):
        super(IncomeStatement, self).__init__()

        # load the UI file
        uic.loadUi('../screens/IncomeStatement.ui', self)

        self.treeWidget = self.findChild(QtWidgets.QTreeWidget, 'treeWidget')   
        self.startDate = self.findChild(QtWidgets.QDateEdit, 'startDate') 
        self.endDate = self.findChild(QtWidgets.QDateEdit, 'endDate')  
        self.generateReport = self.findChild(QtWidgets.QPushButton, 'generateReport')

        # TODO: connect button to function
        self.generateReport.clicked.connect(self.generate_report)


    def generate_report(self):
        # Retrieve date range from date widgets
        start_date = self.startDate.date().toString("yyyy-MM-dd")
        end_date = self.endDate.date().toString("yyyy-MM-dd")

        # Fetch data from database
        data = self.fetch_data(start_date, end_date)
        
        # Populate TreeWidget with data
        self.populate_tree_widget(data)

    def fetch_data(self, start_date, end_date):
        # Database connection
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()
        
        # TODO: complete the query
        query = """
        SELECT account_name, debit, credit 
        FROM income_statement
        WHERE transaction_date BETWEEN ? AND ?
        """
        cursor.execute(query, (start_date, end_date))
        
        data = cursor.fetchall()
        conn.close()
        return data