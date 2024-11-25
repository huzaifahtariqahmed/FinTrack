import sys
from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import Qt
from PyQt6 import QtCore

transactions = [
    ["1", "Expense", "2024-11-01", "Credit Card", "Purchase", "10012345678901", "250.75", "Office Supplies"],
    ["2", "Revenue", "2024-11-02", "Bank Transfer", "Sales", "20023456789012", "5000.00", "Product Sale"],
    ["3", "Expense", "2024-11-03", "Cash", "Payment", "30034567890123", "150.00", "Utility Bill"],
    ["4", "Revenue", "2024-11-04", "PayPal", "Receipt", "40045678901234", "1200.50", "Service Payment"],
    ["5", "Expense", "2024-11-05", "Debit Card", "Purchase", "50056789012345", "375.25", "Travel Expenses"],
    ["6", "Revenue", "2024-11-06", "Cash", "Sales", "60067890123456", "720.00", "Store Sale"],
    ["7", "Expense", "2024-11-07", "Bank Transfer", "Payment", "70078901234567", "480.00", "Subscription Fee"],
    ["8", "Revenue", "2024-11-08", "Credit Card", "Receipt", "80089012345678", "2100.75", "Client Payment"]
]

class Transaction(QtWidgets.QMainWindow):
    def __init__(self):
        # Call the inherited classes __init__ method
        super(Transaction, self).__init__() 
        # Load the .ui file
        uic.loadUi('AutomatedTransactionRecordingModule.ui', self) 
        
        # Set Window Title
        self.setWindowTitle('Transaction Recording Module')
       
        self.transactions_table.setRowCount(len(transactions))
        for i in range(len(transactions)):
            for j in range(8):
                item = QtWidgets.QTableWidgetItem(transactions[i][j])
                # Make the items non-editable
                item.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable) 
                self.transactions_table.setItem(i,j,item)
        # Connect the search function with the search button.
        self.search_button.clicked.connect(self.search)
        
        # Connect the reset function with the reset button.
        self.reset_button.clicked.connect(self.reset)
        
        # Connect the view function with the view button.
        self.view_button.clicked.connect(self.view)

        # Connect the delete function with the delete button.
        self.delete_button.clicked.connect(self.delete)
        
        # Connect the add function with the add button.
        self.add_button.clicked.connect(self.add)

        # # Connect the close function with the close button.
        # self.close_widget.clicked.connect(self.close)
        
    def reset(self):
        # Clear all current table contents
        self.transactions_table.clearContents()
        self.transactions_table.setRowCount(len(transactions))  # Reset the row count to match the original list size

        # Populate the table with the original transactions
        for i, transaction in enumerate(transactions):
            for j, value in enumerate(transaction):
                item = QtWidgets.QTableWidgetItem(str(value))
                item.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable)
                self.transactions_table.setItem(i, j, item)

    
    def search(self):
        # Clear only the table contents, preserving headers
        self.transactions_table.clearContents()
        self.transactions_table.setRowCount(0)  # Reset the row count to zero
        
        # Get search input values
        category = self.category_input.currentText().strip()
        sub_category = self.sub_category_input_2.currentText().strip()
        amount = self.amount_input.text().strip()
        payment_method = self.payment_method_input.text().strip()
        expense_type = self.expense_type_input.text().strip()
        account_number = self.account_number_input.text().strip()
        date = self.date_input.date().toString("yyyy-MM-dd").strip()  # Convert QDate to string

        # Initialize row counter for the filtered results
        count = 0

        # Iterate through transactions and filter
        for transaction in transactions:
            # Perform comparisons; skip if any condition fails
            if (category and category not in transaction[1]) or \
            (sub_category and sub_category not in transaction[4]) or \
            (amount and amount not in str(transaction[6])) or \
            (payment_method and payment_method not in transaction[3]) or \
            (expense_type and expense_type not in transaction[7]) or \
            (account_number and account_number not in str(transaction[5])) or \
            (date and date not in transaction[2]):
                continue
            
            # Add the matching transaction to the table
            self.transactions_table.insertRow(count)
            for j, value in enumerate(transaction):
                item = QtWidgets.QTableWidgetItem(str(value))
                item.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable)
                self.transactions_table.setItem(count, j, item)
            count += 1

        # Display a message if no results are found
        if count == 0:
            QMessageBox.warning(self, "No Results", "No transactions match the search criteria.")             
            
      
    def add(self):
        # Collect data from the input fields
        category = self.category_input.currentText()
        sub_category = self.sub_category_input_2.currentText()
        amount = self.amount_input.text()
        payment_method = self.payment_method_input.text()
        expense_type = self.expense_type_input.text()
        account_number = self.account_number_input.text()
        date = self.date_input.date().toString("yyyy-MM-dd")  # Convert QDate to string

        # Validate the input to ensure no field is empty (You can adjust this validation as needed)
        if not category or not sub_category or not amount or not payment_method or not expense_type or not account_number or not date:
            QMessageBox.warning(self, "Input Error", "Please fill in all fields to add a transaction.")
            return

        # Create a new transaction (all data is treated as strings)
        new_transaction = [
            str(len(transactions) + 1),  # Generate a new transaction ID (assuming IDs are sequential)
            category,
            date,
            payment_method,
            sub_category,
            account_number,  # Account number remains a string
            amount,  # Amount is a string
            expense_type
        ]

        # Add the new transaction to the list
        transactions.append(new_transaction)

        # Update the table to show the new transaction
        row_position = self.transactions_table.rowCount()
        self.transactions_table.insertRow(row_position)  # Insert a new row at the end

        # Fill the new row with the new transaction data
        for col, value in enumerate(new_transaction):
            item = QtWidgets.QTableWidgetItem(str(value))
            item.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable)
            self.transactions_table.setItem(row_position, col, item)

        # Optionally, reset all input fields after adding the transaction
        self.category_input.setCurrentIndex(0)
        self.sub_category_input_2.setCurrentIndex(0)
        self.amount_input.clear()
        self.payment_method_input.clear()
        self.expense_type_input.clear()
        self.account_number_input.clear()
        self.date_input.setDate(QtCore.QDate.currentDate())
      
    def delete(self):
        # Get the selected row
        selected_row = self.transactions_table.currentRow()

        # Check if a row is selected
        if selected_row >= 0:
            # Remove the corresponding transaction from the list
            del transactions[selected_row]

            # Remove the selected row from the table
            self.transactions_table.removeRow(selected_row)

            # Optionally, show a confirmation message
            QMessageBox.information(self, "Success", "Transaction deleted successfully.")
        else:
            # If no row is selected, show a warning message
            QMessageBox.warning(self, "No Selection", "Please select a transaction to delete.")

            
    def view(self):
        if(self.transactions_table.selectedIndexes()!=0):
            row = self.transactions_table.currentRow()
            id = self.transactions_table.item(row,0).text()
            category = self.transactions_table.item(row,1).text()
            date = self.transactions_table.item(row,2).text()
            payment_method = self.transactions_table.item(row,3).text()
            sub_category = self.transactions_table.item(row,4).text()
            account_number = self.transactions_table.item(row,5).text()
            amount = self.transactions_table.item(row,6).text()
            expense_type = self.transactions_table.item(row,7).text()
        
        # Pass all the data to view form as parameters
        self.view_form = ViewTransaction(id, category, date, payment_method, sub_category, account_number, amount, expense_type)
        self.view_form.show()     
            

class ViewTransaction(QtWidgets.QMainWindow):  
    def __init__(self, id, category, date, payment_method, sub_category, account_number, amount, expense_type):
        super().__init__()
        uic.loadUi('ViewTransaction.ui', self)

        # Receive Data from the Main Form
        self.id = id
        self.category = category
        self.date = date
        self.payment_method = payment_method
        self.sub_category = sub_category
        self.account_number = account_number
        self.amount = amount
        self.expense_type = expense_type

        # Set Window Title
        self.setWindowTitle('View Transaction')

        self.id_input.setText(self.id)
        self.category_input.setText(self.category)
        self.date_input.setDate(QtCore.QDate.fromString(self.date, "yyyy-MM-dd"))
        self.payment_method_input.setText(self.payment_method)
        self.sub_category_input.setText(self.sub_category)
        self.account_number_input.setText(self.account_number)
        self.amount_input.setText(self.amount)
        self.expense_type_input.setText(self.expense_type)
        
        self.id_input.setReadOnly(True)
        self.category_input.setReadOnly(True)
        self.date_input.setReadOnly(True)
        self.payment_method_input.setReadOnly(True)
        self.sub_category_input.setReadOnly(True)
        self.account_number_input.setReadOnly(True)
        self.amount_input.setReadOnly(True)
        self.expense_type_input.setReadOnly(True)
        
    def view_account_info(self):
        if(self.transactions_table.selectedIndexes()!=0):
            row = self.transactions_table.currentRow()
            id = self.transactions_table.item(row,0).text()
            category = self.transactions_table.item(row,1).text()
            date = self.transactions_table.item(row,2).text()
            payment_method = self.transactions_table.item(row,3).text()
            sub_category = self.transactions_table.item(row,4).text()
            account_number = self.transactions_table.item(row,5).text()
            amount = self.transactions_table.item(row,6).text()
            expense_type = self.transactions_table.item(row,7).text()
        
        # Pass all the data to view form as parameters
        self.view_form = ViewAccountInfo(id, category, date, payment_method, sub_category, account_number, amount, expense_type)
        self.view_form.show() 
        
class ViewAccountInfo(QtWidgets.QMainWindow):  
    def __init__(self, id, category, date, payment_method, sub_category, account_number, amount, expense_type):
        super().__init__()
        uic.loadUi('AccountInfo.ui', self)


app = QtWidgets.QApplication(sys.argv) # Create an instance of QtWidgets.QApplication
window = Transaction() # Create an instance of our 
window.show()
app.exec() # Start the application