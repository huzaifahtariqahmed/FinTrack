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


class Transaction(QtWidgets.QMainWindow):
    def __init__(self, connection_string):
        # Call the inherited classes __init__ method
        super(Transaction, self).__init__() 
        # Load the .ui file
        uic.loadUi('../../screens/AutomatedTransactionRecordingModule.ui', self) 
        
        self.connection_string = connection_string

        # Set Window Title
        self.setWindowTitle('Transaction Recording Module')

        connection = pyodbc.connect(self.connection_string)
        cursor = connection.cursor()
        cursor.execute("""select T.TRANSACTION_ID, C.CATEGORY_NAME, CONVERT(DATE, T.TRANSACTION_DATE) as 'Date', P.PAYMENT_METHOD_NAME, S.SUB_CATEGORY_NAME, A.ACCOUNT_NUM, T.TRANSACTION_AMOUNT, E.EXPENSE_TITLE
                        FROM [TRANSACTION] T
                        inner join PaymentMethod P on P.PAYMENT_METHOD_ID = T.FK_PAYMENT_METHOD_ID
                        inner join ExpenseType E on T.FK_EXPENSE_ID = E.EXPENSE_ID
                        inner join SubCategory S on E.FK_SUB_CATEGORY_ID = S.SUB_CATEGORY_ID
                        inner join Category C on C.CATEGORY_ID = S.FK_CATEGORY_ID
                        left join Account A on A.ACCOUNT_ID = T.FK_ACCOUNT_ID""")
        

        self.transactions_table.clearContents()
        self.transactions_table.setRowCount(0)
        # Fetch all rows and populate the table
        for row_index, row_data in enumerate(cursor.fetchall()):
            self.transactions_table.insertRow(row_index)
            for col_index, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                self.transactions_table.setItem(row_index, col_index, item)

        # Allow clearing the field
        self.date_input.setSpecialValueText("")  # Show empty placeholder
        # self.date_input.clear()

        # Close the database connection
        connection.close()

        # Adjust content display
        header = self.transactions_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)

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

        # Connect the close function with the close button.
        self.close_button.clicked.connect(self.end)

    def end(self):
        self.close()

    def update(self):
        connection = pyodbc.connect(self.connection_string)
        cursor = connection.cursor()
        cursor.execute("""select T.TRANSACTION_ID, C.CATEGORY_NAME, CONVERT(DATE, T.TRANSACTION_DATE) as 'Date', P.PAYMENT_METHOD_NAME, S.SUB_CATEGORY_NAME, A.ACCOUNT_NUM, T.TRANSACTION_AMOUNT, E.EXPENSE_TITLE
                        FROM [TRANSACTION] T
                        inner join PaymentMethod P on P.PAYMENT_METHOD_ID = T.FK_PAYMENT_METHOD_ID
                        inner join ExpenseType E on T.FK_EXPENSE_ID = E.EXPENSE_ID
                        inner join SubCategory S on E.FK_SUB_CATEGORY_ID = S.SUB_CATEGORY_ID
                        inner join Category C on C.CATEGORY_ID = S.FK_CATEGORY_ID
                        left join Account A on A.ACCOUNT_ID = T.FK_ACCOUNT_ID""")

        self.transactions_table.clearContents()
        self.transactions_table.setRowCount(0)
        # Fetch all rows and populate the table
        for row_index, row_data in enumerate(cursor.fetchall()):
            self.transactions_table.insertRow(row_index)
            for col_index, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                self.transactions_table.setItem(row_index, col_index, item)

        
        # Close the database connection
        connection.close()
        
    def reset(self):
        connection = pyodbc.connect(self.connection_string)
        cursor = connection.cursor()
        cursor.execute("""select T.TRANSACTION_ID, C.CATEGORY_NAME, CONVERT(DATE, T.TRANSACTION_DATE) as 'Date', P.PAYMENT_METHOD_NAME, S.SUB_CATEGORY_NAME, A.ACCOUNT_NUM, T.TRANSACTION_AMOUNT, E.EXPENSE_TITLE
                        FROM [TRANSACTION] T
                        inner join PaymentMethod P on P.PAYMENT_METHOD_ID = T.FK_PAYMENT_METHOD_ID
                        inner join ExpenseType E on T.FK_EXPENSE_ID = E.EXPENSE_ID
                        inner join SubCategory S on E.FK_SUB_CATEGORY_ID = S.SUB_CATEGORY_ID
                        inner join Category C on C.CATEGORY_ID = S.FK_CATEGORY_ID
                        left join Account A on A.ACCOUNT_ID = T.FK_ACCOUNT_ID""")

        self.transactions_table.clearContents()
        self.transactions_table.setRowCount(0)
        # Fetch all rows and populate the table
        for row_index, row_data in enumerate(cursor.fetchall()):
            self.transactions_table.insertRow(row_index)
            for col_index, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                self.transactions_table.setItem(row_index, col_index, item)

    
    # def search(self):
    #     # Clear only the table contents, preserving headers
    #     self.transactions_table.clearContents()
    #     self.transactions_table.setRowCount(0)  # Reset the row count to zero
        
    #     # Get search input values
    #     category = self.category_input.currentText().strip()
    #     sub_category = self.sub_category_input_2.currentText().strip()

    #     connection = pyodbc.connect(self.connection_string)
    #     cursor = connection.cursor()
    #     query = """select T.TRANSACTION_ID, C.CATEGORY_NAME, CONVERT(DATE, T.TRANSACTION_DATE) as 'Date', P.PAYMENT_METHOD_NAME, S.SUB_CATEGORY_NAME, A.ACCOUNT_NUM, T.TRANSACTION_AMOUNT, E.EXPENSE_TITLE
    #                     FROM [TRANSACTION] T
    #                     inner join PaymentMethod P on P.PAYMENT_METHOD_ID = T.FK_PAYMENT_METHOD_ID
    #                     inner join ExpenseType E on T.FK_EXPENSE_ID = E.EXPENSE_ID
    #                     inner join SubCategory S on E.FK_SUB_CATEGORY_ID = S.SUB_CATEGORY_ID
    #                     inner join Category C on C.CATEGORY_ID = S.FK_CATEGORY_ID
    #                     left join Account A on A.ACCOUNT_ID = T.FK_ACCOUNT_ID
    #                     where 
    #                     C.CATEGORY_NAME = ? and S.SUB_CATEGORY_NAME = ?
    #                     """
        
    #     cursor.execute(query, (category, sub_category,))

    #     self.transactions_table.clearContents()
    #     self.transactions_table.setRowCount(0)
               
    #     # Fetch all rows and populate the table
    #     for row_index, row_data in enumerate(cursor.fetchall()):
    #         self.transactions_table.insertRow(row_index)
    #         for col_index, cell_data in enumerate(row_data):
    #             item = QTableWidgetItem(str(cell_data))
    #             self.transactions_table.setItem(row_index, col_index, item)

    #     # Close the database connection
    #     connection.close()
        
    #     # Adjust content display
    #     header = self.transactions_table.horizontalHeader()
    #     header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
    #     header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
    #     header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)      

    def search(self):
        # Clear only the table contents, preserving headers
        self.transactions_table.clearContents()
        self.transactions_table.setRowCount(0)  # Reset the row count to zero

        # Get search input values from UI components
        category = self.category_input.currentText().strip()
        sub_category = self.sub_category_input_2.currentText().strip()
        transaction_date = self.date_input.date().toString("yyyy-MM-dd") if self.date_input.date() else None
        payment_method = self.payment_method_input.currentText().strip()
        account_num = self.account_number_input.text().strip()
        transaction_amount = self.amount_input.text().strip()
        expense_type = self.expense_type_input.currentText().strip()

        print(category, sub_category, transaction_date, payment_method, account_num, transaction_amount, expense_type)

        # Connect to the database
        connection = pyodbc.connect(self.connection_string)
        cursor = connection.cursor()

        # Base query
        query = """
            SELECT T.TRANSACTION_ID,
                C.CATEGORY_NAME, 
                CONVERT(DATE, T.TRANSACTION_DATE) AS 'Date', 
                P.PAYMENT_METHOD_NAME, 
                S.SUB_CATEGORY_NAME, 
                A.ACCOUNT_NUM, 
                T.TRANSACTION_AMOUNT, 
                E.EXPENSE_TITLE
            FROM [TRANSACTION] T
            INNER JOIN PaymentMethod P ON P.PAYMENT_METHOD_ID = T.FK_PAYMENT_METHOD_ID
            INNER JOIN ExpenseType E ON T.FK_EXPENSE_ID = E.EXPENSE_ID
            INNER JOIN SubCategory S ON E.FK_SUB_CATEGORY_ID = S.SUB_CATEGORY_ID
            INNER JOIN Category C ON C.CATEGORY_ID = S.FK_CATEGORY_ID
            LEFT JOIN Account A ON A.ACCOUNT_ID = T.FK_ACCOUNT_ID
            WHERE 1=1
        """

        # Dynamic filter conditions
        params = []

        if category:
            query += " AND C.CATEGORY_NAME = ?"
            params.append(category)
        if sub_category:
            query += " AND S.SUB_CATEGORY_NAME = ?"
            params.append(sub_category)
        if transaction_date:
            query += " AND CONVERT(DATE, T.TRANSACTION_DATE) = ?"
            params.append(transaction_date)
        if payment_method:
            query += " AND P.PAYMENT_METHOD_NAME = ?"
            params.append(payment_method)
        if account_num:
            query += " AND A.ACCOUNT_NUM = ?"
            params.append(account_num)
        if transaction_amount:
            query += " AND T.TRANSACTION_AMOUNT = ?"
            params.append(transaction_amount)
        if expense_type:
            query += " AND E.EXPENSE_TITLE LIKE ?"
            params.append(expense_type)  # Use LIKE for partial matching

        # Execute the query with dynamic parameters
        cursor.execute(query, params)

        # Fetch all rows and populate the table
        for row_index, row_data in enumerate(cursor.fetchall()):
            self.transactions_table.insertRow(row_index)
            for col_index, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                self.transactions_table.setItem(row_index, col_index, item)

        # Close the database connection
        connection.close()

        # Adjust content display
        header = self.transactions_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)  
    def add(self):
        # Pass all the data to view form as parameters
        self.add_form = AddTransaction(self, self.connection_string)
        self.add_form.show()     

       
    def delete(self):

        dig = QMessageBox(self)
        dig.setWindowTitle("Confirmation Box")
        dig.setText("Are you sure you want to delete this transaction?")
        dig.setIcon(QMessageBox.Icon.Warning)
        dig.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        response = dig.exec()

        if response == QMessageBox.StandardButton.Yes:
            current_row = self.transactions_table.currentRow()
            if current_row >= 0:  # Check if a valid row is selected
                id = self.transactions_table.item(current_row, 0).text()
                
                try:
                    connection = pyodbc.connect(self.connection_string)
                    cursor = connection.cursor()
                    
                    # Check if the transaction exists
                    cursor.execute("SELECT COUNT(*) FROM [Transaction] WHERE Transaction_ID = ?", (id,))
                    count = cursor.fetchone()[0]
                    if count == 0:
                        QMessageBox.warning(self, "Error", "Transaction not found")
                        return
                    
                    # Proceed with the delete query
                    query = """DELETE FROM [Transaction] WHERE Transaction_ID = ?"""
                    cursor.execute(query, (id,))
                    
                    # Commit the transaction to apply the changes
                    connection.commit()

                except pyodbc.Error as e:
                    print("Database error:", e)
                    QMessageBox.warning(self, "Database Error", "An error occurred while deleting the transaction.")
                finally:
                    if cursor:
                        cursor.close()
                    if connection:
                        connection.close()

                self.update()  # Assuming this is a valid method to update the UI
            else:
                QMessageBox.warning(self, "Error", "No transaction selected")
        

            
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
        uic.loadUi('../../screens/ViewTransaction.ui', self)

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
        
        # Connect the close function with the close button.
        self.close_button.clicked.connect(self.end)

    def end(self):
        self.close()

class AddTransaction(QtWidgets.QMainWindow):  
    def __init__(self, parent_window, connection_string):
        super().__init__()
        uic.loadUi('../../screens/AddTransaction.ui', self)

        # Set Window Title
        self.setWindowTitle('Add Transaction')

        self.parent_window = parent_window
        self.connection_string = connection_string
        
        # Connect the close function with the close button.
        self.close_button.clicked.connect(self.end)

        self.save_button.clicked.connect(self.save)


    def save(self):

        # Collect data from the input fields
        amount = float(self.amount_input.text())
        payment_method = self.payment_method_input.currentText()
        expense_type = self.expense_type_input.currentText()
        account_number = self.account_number_input.text()
        date = self.date_input.date().toPyDate()  # Convert QDate to string

        print(type(amount))
        print(amount, payment_method, expense_type, account_number, date)


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
                INSERT INTO [Transaction] (TRANSACTION_DATE, FK_PAYMENT_METHOD_ID, FK_ACCOUNT_ID, TRANSACTION_AMOUNT, FK_EXPENSE_ID)
                VALUES (?, 
                        (SELECT P.PAYMENT_METHOD_ID FROM PaymentMethod P WHERE PAYMENT_METHOD_NAME = ?), 
                        (SELECT A.ACCOUNT_ID FROM ACCOUNT A WHERE ACCOUNT_NUM = ?), ?, 
                        (SELECT E.EXPENSE_ID FROM EXPENSETYPE E WHERE EXPENSE_TITLE = ?))
            """, (date, payment_method, account_number, amount, expense_type))
            connection.commit()  # Commit if the insert was successful
        except Exception as e:
            print("Error executing insert:", e)
            connection.rollback()  # Rollback in case of error

                # Close the database connection
        connection.close()

        # Update the table in the parent window
        self.parent_window.update()
        # Show a success message and close the window
        QtWidgets.QMessageBox.information(self, "Success", "Transaction Updated Successfully")
        self.close()

    def end(self):
        self.close()
