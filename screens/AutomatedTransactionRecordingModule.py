import sys
from PyQt6 import QtWidgets, uic

class Transactions(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        # Load the UI file created in Qt Designer
        uic.loadUi("AutomatedTransactionRecordingModule.ui", self)
        
        # Initialize an in-memory list to hold transactions
        self.transactions = []

        # Connect buttons to their respective methods
        self.view_button.clicked.connect(self.view_transactions)
        self.add_button.clicked.connect(self.add_transaction)
        self.delete_button.clicked.connect(self.delete_transaction)
        self.search_button.clicked.connect(self.search_transactions)

    def view_transactions(self):
        """Displays all transactions in the table."""
        self.transactions_table.setRowCount(0)  # Clear the table first
        for row_number, transaction in enumerate(self.transactions):
            self.transactions_table.insertRow(row_number)
            for column_number, data in enumerate(transaction):
                self.transactions_table.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))

    def add_transaction(self):
        """Adds a new transaction to the in-memory list."""
        transaction_id = len(self.transactions) + 1
        category = self.category_input.text()
        date = self.date_input.text()
        payment_method = self.payment_method_input.text()
        sub_category = self.sub_category_input.text()
        account_number = self.account_number_input.text()
        amount = self.amount_input.text()
        expense_type = self.expense_type_input.text()

        # Ensure all fields are filled
        if not all([category, date, payment_method, sub_category, account_number, amount, expense_type]):
            QtWidgets.QMessageBox.warning(self, "Error", "All fields must be filled!")
            return

        # Add the transaction to the in-memory list
        self.transactions.append([
            transaction_id, category, date, payment_method,
            sub_category, account_number, float(amount), expense_type
        ])
        self.view_transactions()  # Refresh the table
        QtWidgets.QMessageBox.information(self, "Success", "Transaction added successfully!")

    def delete_transaction(self):
        """Deletes the selected transaction from the in-memory list."""
        selected_row = self.transactions_table.currentRow()
        if selected_row < 0:
            QtWidgets.QMessageBox.warning(self, "Error", "No row selected!")
            return

        # Remove the selected transaction from the list
        del self.transactions[selected_row]
        self.view_transactions()  # Refresh the table
        QtWidgets.QMessageBox.information(self, "Success", "Transaction deleted successfully!")

    def search_transactions(self):
        """Searches for transactions based on category and sub-category inputs."""
        category = self.category_input.text()
        sub_category = self.sub_category_input.text()

        filtered_transactions = [
            transaction for transaction in self.transactions
            if (not category or transaction[1] == category) and
               (not sub_category or transaction[4] == sub_category)
        ]

        # Display filtered transactions
        self.transactions_table.setRowCount(0)
        for row_number, transaction in enumerate(filtered_transactions):
            self.transactions_table.insertRow(row_number)
            for column_number, data in enumerate(transaction):
                self.transactions_table.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Transactions()
    window.show()
    sys.exit(app.exec())
