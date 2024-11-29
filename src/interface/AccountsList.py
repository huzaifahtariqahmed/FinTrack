from PyQt6 import QtWidgets, uic, QtCore
from PyQt6.QtCore import QDate, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QHeaderView , QMessageBox
import sys
import pyodbc

# Replace these with your own database connection details
server = 'DESKTOP-6M55HJA\\SQLSERVER1'
database = 'Fintrack'  # Name of your Fintrack database
use_windows_authentication = True  # Set to True to use Windows Authentication
username = 'sa'  # Specify a username if not using Windows Authentication
password = '1234'  # Specify a password if not using Windows Authentication

#  Create the connection string based on the authentication method chosen
if use_windows_authentication:
    connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
else:
    connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'

class Accounts(QtWidgets.QMainWindow):
    def __init__(self, connection_string):
        # Call the inherited classes __init__ method
        super(Accounts, self).__init__() 
        # Load the .ui file
        uic.loadUi('../../screens/AccountsList.ui', self) 
        
        self.connection_string = connection_string

        # Set Window Title
        self.setWindowTitle('Accounts List Module')

        connection = pyodbc.connect(self.connection_string)
        cursor = connection.cursor()
        cursor.execute("""select A.ACCOUNT_ID, A.ACCOUNT_TITLE, A.ACCOUNT_NUM, (SUM(CASE WHEN S.FK_CATEGORY_ID = 4 THEN T.TRANSACTION_AMOUNT WHEN S.FK_CATEGORY_ID = 3 THEN -T.TRANSACTION_AMOUNT END)) AS ACCOUNT_BALANCE
                        FROM ACCOUNT A
                        left join [Transaction] T on T.FK_ACCOUNT_ID = A.ACCOUNT_ID
                        left join ExpenseType E on T.FK_EXPENSE_ID = E.EXPENSE_ID
                        left join SubCategory S on E.FK_SUB_CATEGORY_ID = S.SUB_CATEGORY_ID
						GROUP BY A.ACCOUNT_ID, A.ACCOUNT_TITLE, A.ACCOUNT_NUM""")

        self.accounts_table.clearContents()
        self.accounts_table.setRowCount(0)
        # Fetch all rows and populate the table
        for row_index, row_data in enumerate(cursor.fetchall()):
            self.accounts_table.insertRow(row_index)
            for col_index, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                self.accounts_table.setItem(row_index, col_index, item)

        
        # Close the database connection
        connection.close()

        # Adjust content display
        header = self.accounts_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        
        # Connect the view function with the view button.
        self.view_button.clicked.connect(self.view)

        # Connect the delete function with the delete button.
        self.delete_button.clicked.connect(self.delete)
        
        # Connect the add function with the add button.
        self.add_button.clicked.connect(self.add)

        # Connect the close function with the close button.
        self.close_button.clicked.connect(self.end)

    def end(self):
        self.close()
        
    # def reset(self):
    #     # Clear all current table contents
    #     self.accounts_table.clearContents()
    #     self.accounts_table.setRowCount(len(accounts))  # Reset the row count to match the original list size

    #     # Populate the table with the original transactions
    #     for i, transaction in enumerate(accounts):
    #         for j, value in enumerate(transaction):
    #             item = QtWidgets.QTableWidgetItem(str(value))
    #             item.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable)
    #             self.accounts_table.setItem(i, j, item)

    
    # def search(self):
    #     # Clear only the table contents, preserving headers
    #     self.accounts_table.clearContents()
    #     self.accounts_table.setRowCount(0)  # Reset the row count to zero
        
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
    #         self.accounts_table.insertRow(count)
    #         for j, value in enumerate(transaction):
    #             item = QtWidgets.QTableWidgetItem(str(value))
    #             item.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable)
    #             self.accounts_table.setItem(count, j, item)
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
    #     row_position = self.accounts_table.rowCount()
    #     self.accounts_table.insertRow(row_position)  # Insert a new row at the end

    #     # Fill the new row with the new transaction data
    #     for col, value in enumerate(new_transaction):
    #         item = QtWidgets.QTableWidgetItem(str(value))
    #         item.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable)
    #         self.accounts_table.setItem(row_position, col, item)

    #     # Optionally, reset all input fields after adding the transaction
    #     self.category_input.setCurrentIndex(0)
    #     self.sub_category_input_2.setCurrentIndex(0)
    #     self.amount_input.clear()
    #     self.payment_method_input.clear()
    #     self.expense_type_input.clear()
    #     self.account_number_input.clear()
    #     self.date_input.setDate(QtCore.QDate.currentDate())
        
      
    def delete(self):
        dig = QMessageBox(self)
        dig.setWindowTitle("Confirmation Box")
        dig.setText("Are you sure you want to delete this Account?")
        dig.setIcon(QMessageBox.Icon.Warning)
        dig.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        response = dig.exec()

        if response == QMessageBox.StandardButton.Yes:
            current_row = self.accounts_table.currentRow()
            if current_row >= 0:  # Check if a valid row is selected
                id = self.accounts_table.item(current_row, 0).text()
                
                try:
                    connection = pyodbc.connect(self.connection_string)
                    cursor = connection.cursor()
                    
                    # Check if the transaction exists
                    cursor.execute("SELECT COUNT(*) FROM Account WHERE Account_ID = ?", (id,))
                    count = cursor.fetchone()[0]
                    if count == 0:
                        QMessageBox.warning(self, "Error", "Account not found")
                        return
                    
                    # Proceed with the delete query
                    query = """DELETE FROM Account WHERE Account_ID = ?"""
                    cursor.execute(query, (id,))
                    
                    # Commit the transaction to apply the changes
                    connection.commit()

                except pyodbc.Error as e:
                    print("Database error:", e)
                    QMessageBox.warning(self, "Database Error", "An error occurred while deleting the account.")
                finally:
                    if cursor:
                        cursor.close()
                    if connection:
                        connection.close()

                self.update()  # Assuming this is a valid method to update the UI
            else:
                QMessageBox.warning(self, "Error", "No account selected")
            
        
            
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
            
    def add(self):
            
        # Pass all the data to view form as parameters
        self.add_form = AddAccountInfo(self, self.connection_string)
        self.add_form.show()    
        
    def update(self):
        connection = pyodbc.connect(self.connection_string)
        cursor = connection.cursor()
        cursor.execute("""select A.ACCOUNT_ID, A.ACCOUNT_TITLE, A.ACCOUNT_NUM, (SUM(CASE WHEN S.FK_CATEGORY_ID = 4 THEN T.TRANSACTION_AMOUNT WHEN S.FK_CATEGORY_ID = 3 THEN -T.TRANSACTION_AMOUNT END)) AS ACCOUNT_BALANCE
                        FROM ACCOUNT A
                        left join [Transaction] T on T.FK_ACCOUNT_ID = A.ACCOUNT_ID
                        left join ExpenseType E on T.FK_EXPENSE_ID = E.EXPENSE_ID
                        left join SubCategory S on E.FK_SUB_CATEGORY_ID = S.SUB_CATEGORY_ID
						GROUP BY A.ACCOUNT_ID, A.ACCOUNT_TITLE, A.ACCOUNT_NUM""")

        self.accounts_table.clearContents()
        self.accounts_table.setRowCount(0)
        # Fetch all rows and populate the table
        for row_index, row_data in enumerate(cursor.fetchall()):
            self.accounts_table.insertRow(row_index)
            for col_index, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                self.accounts_table.setItem(row_index, col_index, item)

        
        # Close the database connection
        connection.close()

class ViewAccountInfo(QtWidgets.QMainWindow):  
    def __init__(self, account_id, account_title, account_number, account_balance):
        super().__init__()
        uic.loadUi('../../screens/AccountInfo.ui', self)

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
        self.close_button.clicked.connect(self.end)

    def end(self):
        self.close()
        
class AddAccountInfo(QtWidgets.QMainWindow):  
    def __init__(self, parent_window, connection_string):
        super().__init__()
        uic.loadUi('../../screens/AddAccountInfo.ui', self)

        self.parent_window = parent_window
        self.connection_string = connection_string

        # Set Window Title
        self.setWindowTitle('Add Account Info')

        # Connect the close function with the close button.
        self.close_button.clicked.connect(self.end)

        # self.save_button.clicked.connect(self.save(date, payment_method, account_number, amount, expense_type))
        self.save_button.clicked.connect(self.save)


    def end(self):
        self.close()

    def save(self):

         # Collect data from the input fields
        account_title = self.account_title_input.text()
        account_num = self.account_number_input.text()


        connection = pyodbc.connect(self.connection_string)
        cursor = connection.cursor()
        
        # # Insert the new transaction into the database
        # cursor.execute("""
        #     INSERT INTO [Transaction] (TRANSACTION_DATE, FK_PAYMENT_METHOD_ID, FK_ACCOUNT_ID, TRANSACTION_AMOUNT, FK_EXPENSE_ID)
        #     VALUES (?, (SELECT P.PAYMENT_METHOD_ID FROM PaymentMethod P WHERE PAYMENT_METHOD_NAME = ?), 
        #                (SELECT A.ACCOUNT_ID FROM ACCOUNT A WHERE ACCOUNT_NUM = ?), ?, 
        #                (SELECT E.EXPENSE_ID FROM EXPENSETYPE E WHERE EXPENSE_TITLE = ?))
        # """, (date, payment_method, account_number, amount, expense_type))

        try:
            cursor.execute("""
                INSERT INTO Account (ACCOUNT_TITLE, ACCOUNT_NUM)
                VALUES (?, ?)
            """, (account_title, account_num))
            connection.commit()  # Commit if the insert was successful
        except Exception as e:
            print("Error executing insert:", e)
            connection.rollback()  # Rollback in case of error

                # Close the database connection
        connection.close()

        # Update the table in the parent window
        self.parent_window.update()
        # Show a success message and close the window
        QtWidgets.QMessageBox.information(self, "Success", "Account Added Successfully")
        self.close()


        # # Get the updated values from the input fields
        # updated_title = self.account_title_input.text()
        # updated_number = self.account_number_input.text()
        # updated_balance = self.account_balance_input.text()

        # # Validate the input fields
        # if not updated_title or not updated_number or not updated_balance:
        #     QtWidgets.QMessageBox.warning(self, "Input Error", "All fields must be filled.")
        #     return

        # # Update the account data in the parent window
        # for account in accounts:
        #     if account[0] == self.account_id:  # Match the account ID
        #         account[1] = updated_title
        #         account[2] = updated_number
        #         account[3] = updated_balance
        #         break

        # # Update the table in the parent window
        # self.parent_window.update_table()

        # # Show a success message and close the window
        # QtWidgets.QMessageBox.information(self, "Success", "Account information updated successfully.")
        # self.close()

# app = QtWidgets.QApplication(sys.argv) # Create an instance of QtWidgets.QApplication
# window = Accounts(connection_string) # Create an instance of our 
# window.show()
# app.exec() # Start the application