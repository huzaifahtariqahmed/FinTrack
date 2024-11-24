# Importing essential modules
from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QHeaderView
import sys
import pyodbc

# FOR GENERATING A CONNECTION STRING
server = 'DESKTOP-6M55HJA\\SQLSERVER1'
database = 'FinTrack'  # Name of your Northwind database
use_windows_authentication = True  # Set to True to use Windows Authentication
username = 'your_username'  # Specify a username if not using Windows Authentication
password = 'your_password'  # Specify a password if not using Windows Authentication


# Create the connection string based on the authentication method chosen
if use_windows_authentication:
    connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
else:
    connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'


class CashFlowStatement(QtWidgets.QMainWindow):
    def __init__(self):
        super(CashFlowStatement, self).__init__()

        # load the UI file
        uic.loadUi('../../screens/FinancialReportingModule.ui', self)

        self.tableWidget.setColumnWidth(0, 250)  # Set width for column 1
        self.tableWidget.setColumnWidthclear(1, 100)  # Set width for column 2

        # TODO: connect button to function
        # self.generateReport.clicked.connect(self.generate_report)
        # self.saveReport.clicked.connect(self.save_report)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = CashFlowStatement()
    window.show()
    sys.exit(app.exec())
