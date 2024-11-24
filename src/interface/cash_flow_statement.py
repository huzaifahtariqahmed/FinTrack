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
        self.tableWidget.setColumnWidth(1, 100)  # Set width for column 2

        # TODO: connect button to function
        # self.generateReport.clicked.connect(self.generate_report)
        self.saveReport.clicked.connect(self.save_report)

    def generate_report(self):
        # Retrieve date range from date widgets~
        start_date = self.startDate.date().toString("yyyy-MM-dd")
        end_date = self.endDate.date().toString("yyyy-MM-dd")

        # Fetch data from database
        data = self.fetch_data(start_date, end_date)
        
        # Populate TreeWidget with data
        self.populate_table(data)



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

    def populate_table(self, data):
        """
        Populate the QTableWidget with data.
        """
        self.tableWidget.setRowCount(len(data))  # Set row count based on data length
        
        # TODO: replace these dummy calcualtions with actual stuff
        for row_index, row_data in enumerate(data):
            account_name = row_data[0] 
            debit = row_data[1] or 0  
            credit = row_data[2] or 0 
            amount = debit - credit 
            
            # Set column 0 (description)
            item_description = QTableWidgetItem(account_name)
            self.tableWidget.setItem(row_index, 0, item_description)

            # Set column 1 (amount)
            item_amount = QTableWidgetItem(f"{amount:.2f}")
            self.tableWidget.setItem(row_index, 1, item_amount)


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
    window = CashFlowStatement()
    window.show()
    sys.exit(app.exec())
