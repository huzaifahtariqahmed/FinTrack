import sys
from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import Qt
from PyQt6 import QtCore

accounts = [
    ["1", "1001", "John Doe", "10012345678901", "5250.00"],
    ["2", "1002", "Jane Smith", "20023456789012", "1850.75"],
    ["3", "1003", "Alice Johnson", "30034567890123", "12450.32"],
    ["4", "1004", "Robert Brown", "40045678901234", "8320.45"],
    ["5", "1005", "Emily Davis", "50056789012345", "3100.00"],
    ["6", "1006", "Michael Wilson", "60067890123456", "25750.88"],
    ["7", "1007", "Sarah Taylor", "70078901234567", "1500.00"],
    ["8", "1008", "David Martin", "80089012345678", "4875.50"]
]

class Accounts(QtWidgets.QMainWindow):
    def __init__(self):
        # Call the inherited classes __init__ method
        super(Accounts, self).__init__() 
        # Load the .ui file
        uic.loadUi('AccountsList.ui', self) 
        
        # Set Window Title
        self.setWindowTitle('Accounts List Module')
       
        self.accounts_table.setRowCount(len(accounts))
        for i in range(len(accounts)):
            for j in range(5):
                item = QtWidgets.QTableWidgetItem(accounts[i][j])
                # Make the items non-editable
                item.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable) 
                self.accounts_table.setItem(i,j,item)
        # # Connect the search function with the search button.
        # self.search_button.clicked.connect(self.search)
        
        # # Connect the reset function with the reset button.
        # self.reset_button.clicked.connect(self.reset)
        
        # Connect the view function with the view button.
        self.view_button.clicked.connect(self.view)

        # Connect the delete function with the delete button.
        self.delete_button.clicked.connect(self.delete)
        
        # # Connect the add function with the add button.
        # self.add_button.clicked.connect(self.add)

        # Connect the close function with the close button.
        self.close_button.clicked.connect(self.close)
        
    # def reset(self):
    #     # Clear all current table contents
    #     self.transactions_table.clearContents()
    #     self.transactions_table.setRowCount(len(accounts))  # Reset the row count to match the original list size

    #     # Populate the table with the original transactions
    #     for i, transaction in enumerate(accounts):
    #         for j, value in enumerate(transaction):
    #             item = QtWidgets.QTableWidgetItem(str(value))
    #             item.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable)
    #             self.transactions_table.setItem(i, j, item)

    
    # def search(self):
    #     # Clear only the table contents, preserving headers
    #     self.transactions_table.clearContents()
    #     self.transactions_table.setRowCount(0)  # Reset the row count to zero
        
    #     # Get search input values
    #     category = self.category_input.currentText().strip()
    #     sub_category = self.sub_category_input_2.currentText().strip()
    #     amount = self.amount_input.text().strip()
    #     payment_method = self.payment_method_input.text().strip()
    #     expense_type = self.expense_type_input.text().strip()
    #     account_number = self.account_number_input.text().strip()
    #     date = self.date_input.date().toString("yyyy-MM-dd").strip()  # Convert QDate to string

    #     # Initialize row counter for the filtered results
    #     count = 0

    #     # Iterate through transactions and filter
    #     for transaction in transactions:
    #         # Perform comparisons; skip if any condition fails
    #         if (category and category not in transaction[1]) or \
    #         (sub_category and sub_category not in transaction[4]) or \
    #         (amount and amount not in str(transaction[6])) or \
    #         (payment_method and payment_method not in transaction[3]) or \
    #         (expense_type and expense_type not in transaction[7]) or \
    #         (account_number and account_number not in str(transaction[5])) or \
    #         (date and date not in transaction[2]):
    #             continue
            
    #         # Add the matching transaction to the table
    #         self.transactions_table.insertRow(count)
    #         for j, value in enumerate(transaction):
    #             item = QtWidgets.QTableWidgetItem(str(value))
    #             item.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable)
    #             self.transactions_table.setItem(count, j, item)
    #         count += 1

    #     # Display a message if no results are found
    #     if count == 0:
    #         QMessageBox.warning(self, "No Results", "No transactions match the search criteria.")             
            
      
    # def add(self):
    #     # Collect data from the input fields
    #     category = self.category_input.currentText()
    #     sub_category = self.sub_category_input_2.currentText()
    #     amount = self.amount_input.text()
    #     payment_method = self.payment_method_input.text()
    #     expense_type = self.expense_type_input.text()
    #     account_number = self.account_number_input.text()
    #     date = self.date_input.date().toString("yyyy-MM-dd")  # Convert QDate to string

    #     # Validate the input to ensure no field is empty (You can adjust this validation as needed)
    #     if not category or not sub_category or not amount or not payment_method or not expense_type or not account_number or not date:
    #         QMessageBox.warning(self, "Input Error", "Please fill in all fields to add a transaction.")
    #         return

    #     # Create a new transaction (all data is treated as strings)
    #     new_transaction = [
    #         str(len(transactions) + 1),  # Generate a new transaction ID (assuming IDs are sequential)
    #         category,
    #         date,
    #         payment_method,
    #         sub_category,
    #         account_number,  # Account number remains a string
    #         amount,  # Amount is a string
    #         expense_type
    #     ]

    #     # Add the new transaction to the list
    #     transactions.append(new_transaction)

    #     # Update the table to show the new transaction
    #     row_position = self.transactions_table.rowCount()
    #     self.transactions_table.insertRow(row_position)  # Insert a new row at the end

    #     # Fill the new row with the new transaction data
    #     for col, value in enumerate(new_transaction):
    #         item = QtWidgets.QTableWidgetItem(str(value))
    #         item.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable)
    #         self.transactions_table.setItem(row_position, col, item)

    #     # Optionally, reset all input fields after adding the transaction
    #     self.category_input.setCurrentIndex(0)
    #     self.sub_category_input_2.setCurrentIndex(0)
    #     self.amount_input.clear()
    #     self.payment_method_input.clear()
    #     self.expense_type_input.clear()
    #     self.account_number_input.clear()
    #     self.date_input.setDate(QtCore.QDate.currentDate())
      
    def delete(self):
        # Get the selected row
        selected_row = self.accounts_table.currentRow()

        # Check if a row is selected
        if selected_row >= 0:
            # Remove the corresponding transaction from the list
            del accounts[selected_row]

            # Remove the selected row from the table
            self.accounts_table.removeRow(selected_row)

            # Optionally, show a confirmation message
            QMessageBox.information(self, "Success", "Transaction deleted successfully.")
        else:
            # If no row is selected, show a warning message
            QMessageBox.warning(self, "No Selection", "Please select a transaction to delete.")
            
    def close(self):
        sys.exit()

            
    def view(self):
        if(self.accounts_table.selectedIndexes()!=0):
            row = self.accounts_table.currentRow()
            account_id = self.accounts_table.item(row,0).text()
            account_title = self.accounts_table.item(row,1).text()
            account_number = self.accounts_table.item(row,2).text()
            account_balance = self.accounts_table.item(row,3).text()

        
        # Pass all the data to view form as parameters
        self.view_form = ViewAccountInfo(account_id, account_title, account_number, account_balance)
        self.view_form.show()     
            

class ViewAccountInfo(QtWidgets.QMainWindow):  
    def __init__(self, account_id, account_title, account_number, account_balance):
        super().__init__()
        uic.loadUi('AccountInfo.ui', self)

        # Receive Data from the Main Form
        self.account_id = account_id
        self.account_title = account_title
        self.account_number = account_number
        self.account_balance = account_balance

        # Set Window Title
        self.setWindowTitle('View Account Info')

        self.account_id_input.setText(self.account_id)
        self.account_title_input.setText(self.account_title)
        self.account_number_input.setText(self.account_number)
        self.account_balance_input.setText(self.account_balance)
        
        self.account_id_input.setReadOnly(True)
        self.account_title_input.setReadOnly(True)
        self.account_number_input.setReadOnly(True)
        self.account_balance_input.setReadOnly(True)
        
        # Connect the close function with the close button.
        self.close_button.clicked.connect(self.close)
        
        # Connect the close function with the close button.
        self.close_button.clicked.connect(self.close)

app = QtWidgets.QApplication(sys.argv) # Create an instance of QtWidgets.QApplication
window = Accounts() # Create an instance of our 
window.show()
app.exec() # Start the application