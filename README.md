# FinTrack: A Comprehensive Accounting Management System :money_with_wings:

FinTrack is an advanced database-driven accounting system designed to streamline financial management
processes for businesses of all sizes. The system provides a robust platform for managing financial
transactions, generating accurate reports, and ensuring compliance with accounting standards. Built using
a relational database, FinTrack enables secure storage, retrieval, and manipulation of financial data,
offering users a reliable tool to monitor and manage their accounts.

FinTrack is an ideal solution for businesses seeking to enhance their accounting processes, improve
financial oversight, and ensure the accuracy of their financial data.

## Repository Structure

```
│   .DS_Store
│   FEATURES.md
│   LICENSE
│   README.md
│
├───docs
├───images
├───screens
└───src
    ├───database
    └───interface
        └───__pycache__
```

## Getting Started

### Requirements
- Python 3.x
- Required Python packages (specified in `requirements.txt`)
- QT Designer
- ODBC Driver 17 for SQL Server for database connectivity
- Microsoft SQL Server Management Studio (SSMS)

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/samiyaalizaidi/FinTrack.git
   cd FinTrack
   ```
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Set up the database in SSMS**:
    - Install SQL Server Management Studio (SSMS)
      -  Download and install from the [official Microsoft Website](https://learn.microsoft.com/en-us/sql/ssms/download-sql-server-management-studio-ssms?view=sql-server-ver16)
    - Open SQL Server Management Studio (SSMS).
    - Create the database.
      - Run ``src/database/script.sql`` in the ``master`` DB to create and populate the database.
      - The database can also be created manually by right-clicking on ``Databases`` in the Object Explorer and selecting ``New Database``  
    - Optional: If the DB was created manually, the dummy data can be populated by running the ``src/database/data.sql`` file in your newly created database.
    - Ensure the database is correctly configured and available for connection.
  
4. **Update the database connection string in** ``src/interface/dashboard.py``:
    
      Replace the following code with your connection details:
    
      ```python
      server = 'DESKTOP-6M55HJA\\SQLSERVER1'  # Update with your server name
      database = 'FinTrack'  # Name of the FinTrack database
      use_windows_authentication = True  # Set to True if using Windows Authentication
      username = 'your_username'  # Specify a username if not using Windows Authentication
      password = 'your_password'  # Specify a password if not using Windows Authentication
      
      # Create the connection string
      if use_windows_authentication:
          connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
      else:
          connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'
      ```
    - **Server**: Replace ``DESKTOP-6M55HJA\\SQLSERVER1`` with your server instance name.
    - **Database**: Replace ``FinTrack`` with your database name if different.
    - **Authentication**:
        - For Windows Authentication: Set ``use_windows_authentication = True``.
        - For SQL Server Authentication: Set ``use_windows_authentication = False`` and provide your username and password.
      
5. **Run the application**
   ```bash
   python src/interface/dashboard.py
   ```

## Features
FinTrack is composed of multiple modules, each designed to address a specific aspect of accounting management. A detailed description of all features can be found in ``FEATURES.md``.

Key highlights include:

- **Intuitive Dashboard**: A central hub for accessing all features.
- **Financial Transactions**: Track income, expenses, and other financial activities.
- **Customizable Reports**: Generate detailed financial statements for any date range.
- **Relational Database Integration**: Secure and efficient storage for your financial data.
  
## Screens and UI
All UI screens for the project are designed using ``.UI`` files, located in the ``/screens`` directory. These are integrated into the application through ``PyQt6``, ensuring a seamless and visually appealing interface.

## Contributors
This project is developed and maintained by:
- [Huzaifah Tariq Ahmed](https://github.com/huzaifahtariqahmed)
- [Daniyal Rahim Areshia](https://github.com/Daniyal-R-A)
- [Samiya Ali Zaidi](https://github.com/samiyaalizaidi)
