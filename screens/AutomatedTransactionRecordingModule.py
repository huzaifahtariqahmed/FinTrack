import sys
from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import Qt

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
        
        # # Connect the view function with the view button.
        # self.view_button.clicked.connect(self.view)

        # # Connect the delete function with the delete button.
        # self.delete_button.clicked.connect(self.delete)
        
        # # Connect the add function with the add button.
        # self.add_button.clicked.connect(self.add)

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
            
#     def view(self):
#         if(self.booksTableWidget.selectedIndexes()!=0):
#             row = self.booksTableWidget.currentRow()
#             isbn = self.booksTableWidget.item(row,0).text()
#             title = self.booksTableWidget.item(row,1).text()
#             category = self.booksTableWidget.item(row,2).text()
#             types = self.booksTableWidget.item(row,3).text()
#             issued = self.booksTableWidget.item(row,4).text()
        
#         # Pass all the data to view form as parameters
#         self.view_form = ViewBook(isbn, title, category, types, issued)
#         self.view_form.show()     
        
#     def delete(self):
#         if(self.booksTableWidget.selectedIndexes()):
#             message = "Are you sure you want to delete this block?"
#             dlg = QMessageBox(self)
#             dlg.setWindowTitle("Confirmation Box")
#             dlg.setText(message)
#             dlg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
#             dlg.setIcon(QMessageBox.Icon.Critical)  
#             # Execute the message box and check which button was clicked
#             result = dlg.exec()
#             if(result == QMessageBox.StandardButton.Yes):
#                 row = self.booksTableWidget.currentRow()
#                 for i in range(len(books)):
#                     if(books[i][0] == self.booksTableWidget.item(row,0).text()):
#                         row = i
#                         break
#                 del books[row]
#                 self.booksTableWidget.clear()
#                 for i in range(len(books)):
#                     for j in range(5):
#                         item = QtWidgets.QTableWidgetItem(books[i][j])
#                         # Make the items non-editable
#                         item.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable) 
#                         self.booksTableWidget.setItem(i,j,item)  
#         else:
#             pass    
           
#     def close(self):
#         sys.exit()
            

# class ViewBook(QtWidgets.QMainWindow):  
#     def __init__(self, isbn, title, category, types, issued):
#         super().__init__()
#         uic.loadUi('ViewBook.ui', self)

#         # Receive Data from the Main Form
#         self.isbn = isbn
#         self.title = title
#         self.category = category
#         self.types = types
#         self.issued = issued

#         # Set Window Title
#         self.setWindowTitle('View Book')

#         self.isbn_widget.setText(self.isbn)
#         self.isbn_widget.setEnabled(False)

#         self.title_widget.setText(self.title)
#         self.title_widget.setEnabled(False)
        
#         self.category_widget.setText(self.category)
#         self.category_widget.setEnabled(False)
        
#         if(self.types == "Reference Book"):
#             self.ref.setChecked(True)
#             self.ref.setEnabled(False)
#         elif(self.types == "Text Book"):
#             self.text.setChecked(True)
#             self.text.setEnabled(False)
#         else:
#             self.journal.setChecked(True)
#             self.journal.setEnabled(False)
            
#         if(self.issued == "True"):
#             self.issued_widget.setChecked(True)
#             self.issued_widget.setEnabled(False)
#         else:
#             self.issued_widget.setChecked(False)
#             self.issued_widget.setEnabled(False)

app = QtWidgets.QApplication(sys.argv) # Create an instance of QtWidgets.QApplication
window = Transaction() # Create an instance of our 
window.show()
app.exec() # Start the application