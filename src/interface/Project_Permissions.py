# Importing essential modules
from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QHeaderView , QMessageBox
import sys
import pyodbc



# Replace these with your own database connection details
server = 'DESKTOP-OJMNK7F\\SQLSERVER1'
database = 'Fintrack'  # Name of your Fintrack database
use_windows_authentication = False  # Set to True to use Windows Authentication
username = 'sa'  # Specify a username if not using Windows Authentication
password = '1234'  # Specify a password if not using Windows Authentication

#  Create the connection string based on the authentication method chosen
if use_windows_authentication:
    connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
else:
    connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'

class PERMISSION(QtWidgets.QMainWindow):
    def __init__(self, connection_string):
        # Call the inherited classes __init__ method
        super(PERMISSION, self).__init__() 
        self.connection_string = connection_string

        self.editPermissionSettings()

    def editPermissionSettings(self):
        #Load the .ui file
        uic.loadUi('../../screens/Project_EditPermissionSettings.ui', self)

        self.setWindowTitle("Edit Permission Settings")

        # Connect to the database
        connection = pyodbc.connect(self.connection_string)
        cursor = connection.cursor()

        # Execute the query to fetch job titles
        cursor.execute("""
        Select P.PERMISSION_NAME
        from Permission P
        """)

        # Clear the table and reset its contents
        self.PermissionTable.clearContents()
        self.PermissionTable.setRowCount(0)

        # Set the column count to match the query result (1 column: JOB_Title)
        self.PermissionTable.setColumnCount(1)  # Explicitly set to 1 column

        # Optional: Set the column header
        self.PermissionTable.setHorizontalHeaderLabels(["Permission Setting"])


        self.PermissionTable.clearContents()
        self.PermissionTable.setRowCount(0)
        # Fetch all rows and populate the table
        for row_index, row_data in enumerate(cursor.fetchall()):
            self.PermissionTable.insertRow(row_index)
            for col_index, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                self.PermissionTable.setItem(row_index, col_index, item)

        # Close the database connection
        connection.close()

        self.DeletePermission_Button.clicked.connect(self.deletePermission)        # Connect the delete function with the delete button.
        self.Close_Button.clicked.connect(self.end)         # Connect the close function with the close button.
        self.AddPermission_Button.clicked.connect(self.addPermission)
        self.EditPermission_Button.clicked.connect(self.editPermission)

        # Adjust content display
        header = self.PermissionTable.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)

    def deletePermission(self):
        dig = QMessageBox(self)
        dig.setWindowTitle("Confirmation Box")
        dig.setText ("Are you sure you want to delete this Permission?")
        dig.setIcon(QMessageBox.Icon.Warning) 
        dig.setStandardButtons (QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No )
        response = dig.exec()

        if response == QMessageBox.StandardButton.Yes:
            PermissionTitlevalue = self.PermissionTable.item(self.PermissionTable.currentRow(), 0).text()
            connection = pyodbc.connect(self.connection_string)
            cursor = connection.cursor()
            query = """Delete from Permission where lower(Permission_Name) = ?"""
            cursor.execute(query, (PermissionTitlevalue.lower(),))     
            # Commit the transaction to apply the changes
            connection.commit()

            # Close the cursor and connection
            cursor.close()
            connection.close()

            self.editPermissionSettings()
    
    def addPermissionTitle(self):
        # Get the text from the input field
        PermissionValue = self.PermissionValue.text().title().strip()

        print(PermissionValue)
        # Check if the input is empty
        if PermissionValue != "":
            # Connect to the database
            connection = pyodbc.connect(self.connection_string)
            cursor = connection.cursor()

            # Define the INSERT query
            query = """
                Insert into Permission (Permission_Name)
                values (?)
            """

            # Execute the query with the parameterized value
            cursor.execute(query, (PermissionValue,))
            
            # Commit the changes
            connection.commit()

            # Provide feedback
            print(f"Permission '{PermissionValue}' added successfully!")

            # Clean up resources
            cursor.close()
            connection.close()

            self.editPermissionSettings()
        else:
            print("Permission cannot be empty!")
            self.editPermissionSettings()  # return to the function again

    def addPermission(self):
        uic.loadUi('../../screens/Project_NewPermission.ui', self)
        # Clear previous content if needed
        self.PermissionValue.clear()
        self.Done_Button.clicked.connect(self.addPermissionTitle)
        self.Cancel_Button.clicked.connect(self.editPermissionSettings)

    def editPermissiontitle(self, Permissionvalue):
        # Get the text from the input field
        prev_val = Permissionvalue
        PermissionValue = self.PermissionValue.text().title().strip()

        print(PermissionValue)
        # Check if the input is empty
        if PermissionValue != "":
            # Connect to the database
            connection = pyodbc.connect(self.connection_string)
            cursor = connection.cursor()

            # Define the update query
            query = """
            UPDATE Permission
            SET Permission_Name = ?
            WHERE LOWER(Permission_Name) = LOWER(?)
            """

            # Execute the update query with parameters
            cursor.execute(query, (PermissionValue.strip(), prev_val.strip()))
            connection.commit()

            print(f"Permission '{prev_val}' successfully updated to '{PermissionValue}'!")

            self.editPermissionSettings()
        else:
            print("Permission cannot be empty!")
            self.editPermissionSettings()  # return to the function again

    def editPermission(self):
      # Clear previous content if needed
        dig = QMessageBox(self)
        dig.setWindowTitle("Confirmation Box")
        dig.setText ("Are you sure you want to edit this Permission?")
        dig.setIcon(QMessageBox.Icon.Warning) 
        dig.setStandardButtons (QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No )
        response = dig.exec()

        if response == QMessageBox.StandardButton.Yes:
            current_val = self.PermissionTable.item(self.PermissionTable.currentRow(), 0).text()
            # print(current_val)
            uic.loadUi('../../screens/Project_NewPermission.ui', self)
            self.PermissionValue.clear()
            self.Done_Button.clicked.connect(lambda: self.editPermissiontitle(current_val))
            self.Cancel_Button.clicked.connect(self.editPermissionSettings)

    def end(self):
        # exit the program
        self.close()


def main():
    app = QApplication(sys.argv)
    window = PERMISSION(connection_string)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
