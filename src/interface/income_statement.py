# Importing essential modules
from PyQt6 import QtWidgets, uic
from PyQt6.QtGui import QFont
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

rows = [
    'Service Charges', 'Product Sales', '        Total Sales Revenue',
    'Office Supplies', 'Utilities', 'Marketing Expense', 
    '        Total Purchase Expense', 'Equipment Payment Expense',
    'Internet Fees', 'Interest Payment', '        Total Operating Expense',
    'Dividends Revenue', '        Total Receipts Revenue', '        Total Revenue',
    'Net Income for FY'
]

special = [
    '        Total Sales Revenue', '        Total Purchase Expense', '        Total Receipts Revenue',
    '        Total Operating Expense', '        Total Revenue', 'Net Income for FY'
]

class IncomeStatement(QtWidgets.QMainWindow):
    def __init__(self):
        super(IncomeStatement, self).__init__()

        # load the UI file
        uic.loadUi('../../screens/IncomeStatement.ui', self)

        self.tableWidget.setColumnWidth(0, 300)  # Set width for column 1
        self.tableWidget.setColumnWidth(1, 100)  # Set width for column 2

        self.generate_report() # generate the initial report

        # TODO: connect button to function
        self.generateReport.clicked.connect(self.generate_report)
        self.saveReport.clicked.connect(self.save_report)


    def generate_report(self):
        # Retrieve date range from date widgets
        start_date = self.startDate.date().toString("yyyy-MM-dd")
        end_date = self.endDate.date().toString("yyyy-MM-dd")

        # Fetch data from database
        data = self.fetch_data(start_date, end_date)
        print(data)

        # Populate TreeWidget with data
        self.populate_table(data)

    def fetch_data(self, start_date, end_date):
        # Database connection
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()
        
        # TODO: complete the query
        query = """
        SELECT 

        SUM(CASE 
            WHEN E.EXPENSE_ID = 15 THEN T.TRANSACTION_AMOUNT -- Service Charges
        END) AS 'Service Charges',

        SUM(CASE 
            WHEN E.EXPENSE_ID = 11 THEN T.TRANSACTION_AMOUNT -- Product Sales
        END) AS 'Product Sales',

        SUM(CASE 
            WHEN sc.SUB_CATEGORY_ID = 6 THEN t.TRANSACTION_AMOUNT -- Total Sales Revenue
        END) AS 'Total Sales Revenue',

        SUM(CASE 
            WHEN E.EXPENSE_ID = 12 THEN T.TRANSACTION_AMOUNT -- Office Supplies
        END) AS 'Office Supplies',

        SUM(CASE 
            WHEN E.EXPENSE_ID = 13 THEN T.TRANSACTION_AMOUNT -- Utilities
        END) AS 'Utilities',

        SUM(CASE 
            WHEN E.EXPENSE_ID = 19 THEN T.TRANSACTION_AMOUNT -- Marketing Expense
        END) AS 'Marketing Expense',

        SUM(CASE 
            WHEN sc.SUB_CATEGORY_ID = 5 THEN t.TRANSACTION_AMOUNT -- Total Purchase Expense
        END) AS 'Total Purchase Expense',

        SUM(CASE 
            WHEN E.EXPENSE_ID = 14 THEN T.TRANSACTION_AMOUNT -- Equipment Payment
        END) AS 'Equipment Payment Expense',

        SUM(CASE 
            WHEN E.EXPENSE_ID = 16 THEN T.TRANSACTION_AMOUNT -- Internet Fees
        END) AS 'Internet Fees',

        SUM(CASE 
            WHEN E.EXPENSE_ID = 17 THEN T.TRANSACTION_AMOUNT -- Internet Payment
        END) AS 'Interest Payment',

        SUM(CASE 
            WHEN sc.SUB_CATEGORY_ID = 7 THEN t.TRANSACTION_AMOUNT -- Total Purchase Expense
        END) AS 'Payment Expense',

        SUM(CASE 
            WHEN E.EXPENSE_ID = 18 THEN T.TRANSACTION_AMOUNT -- Dividends Revenue
        END) AS 'Dividends Revenue',

        SUM(CASE 
            WHEN sc.FK_CATEGORY_ID = 8 THEN t.TRANSACTION_AMOUNT -- Receipts Revenue
        END) AS 'Receipts Revenue',

        SUM(CASE 
            WHEN sc.FK_CATEGORY_ID = 4 THEN t.TRANSACTION_AMOUNT -- Total Revenue
        END) AS 'Revenue',

        SUM(CASE 
            WHEN sc.FK_CATEGORY_ID = 4 THEN t.TRANSACTION_AMOUNT -- Revenue
            WHEN sc.FK_CATEGORY_ID = 3 THEN -t.TRANSACTION_AMOUNT -- Expense 
        END) AS 'Gross Revenue'

        FROM [Transaction] T
        INNER JOIN ExpenseType E ON E.EXPENSE_ID = T.FK_EXPENSE_ID
        INNER JOIN [SubCategory] SC ON SC.SUB_CATEGORY_ID = E.FK_SUB_CATEGORY_ID
        WHERE T.TRANSACTION_DATE BETWEEN ? AND ?;
                """

        cursor.execute(query, (start_date, end_date))
        
        data = cursor.fetchall()
        conn.close()

        return data
    
    def populate_table(self, data):
        """
        Populate the QTableWidget with data.
        """
        self.tableWidget.setRowCount(len(data[0]))  # Set row count based on data length

        font = QFont()
        font.setBold(True)
        
        # TODO: replace these dummy calcualtions with actual stuff
        for row_index, row_data in enumerate(data[0]):
            account_name = rows[row_index] 
            if not row_data: row_data = 0
            amount = row_data
            # Set column 0 (description)
            item_description = QTableWidgetItem(account_name)
            self.tableWidget.setItem(row_index, 0, item_description)

            # Set column 1 (amount)
            item_amount = QTableWidgetItem(f"{amount:.2f}")
            self.tableWidget.setItem(row_index, 1, item_amount)

            if account_name in special:
                item_description.setFont(font)
                item_amount.setFont(font)


    def save_report(self):
        """
        Save the report to a file.
        """
        file_dialog = QtWidgets.QFileDialog()
        file_path, _ = file_dialog.getSaveFileName(self, "Save Report", "", "CSV Files (*.csv);;All Files (*)")
        if file_path:
            with open(file_path, 'w') as file:
                row_count = self.tableWidget.rowCount()
                column_count = self.tableWidget.columnCount()
                for row in range(row_count):
                    row_data = [
                        self.tableWidget.item(row, col).text() if self.tableWidget.item(row, col) else ""
                        for col in range(column_count)
                    ]
                    file.write(",".join(row_data) + "\n")
            print(f"Report saved to {file_path}")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = IncomeStatement()
    window.show()
    sys.exit(app.exec())