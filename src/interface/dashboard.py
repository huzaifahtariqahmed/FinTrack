# Importing essential modules
from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QHeaderView
import sys
from Project import USER
# import pyodbc

# # FOR GENERATING A CONNECTION STRING
# server = 'DESKTOP-6M55HJA\\SQLSERVER1'
# database = 'FinTrack'  # Name of your Northwind database
# use_windows_authentication = True  # Set to True to use Windows Authentication
# username = 'your_username'  # Specify a username if not using Windows Authentication
# password = 'your_password'  # Specify a password if not using Windows Authentication


# # Create the connection string based on the authentication method chosen
# if use_windows_authentication:
#     connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
# else:
#     connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'
    
    
class Dashboard(QtWidgets.QMainWindow):
    def __init__(self):
        super(Dashboard, self).__init__()
        
        # load the UI file
        uic.loadUi('../../screens/Dashboard.ui', self)

        self.setWindowTitle('Dashboard')
        
        # connecting to the user's portal
        self.addUsers.clicked.connect(self.addUsersFunc)
        
        # connecting to the accounts portal
        self.viewAccounts.clicked.connect(self.viewAccountsFunc)
        
        # connecting to the financial module
        self.transactionsButton.clicked.connect(self.transactions)
        self.incomeStatementButton.clicked.connect(self.incomeStatement)
        
        # connecting the close buttons
        self.closeButton.clicked.connect(self.close)
        
    def addUsersFunc(self):
        print("add users button clicked")
        # TODO: Connect Daniyal's screen here
        screen = USER()
        screen.show()
        
        
    def viewAccountsFunc(self):
        print("view accounts button pressed")
        # TODO: Connect huzaifah's account scree here
        
    def transactions(self):
        print("transactions button pressed")
        # TODO: transactions class connection
        
    def incomeStatement(self):
        print("income statement called")
        # TODO: Income statement function called
        
    def close(self):
        print("close")
        
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Dashboard()
    window.show()
    sys.exit(app.exec())
        