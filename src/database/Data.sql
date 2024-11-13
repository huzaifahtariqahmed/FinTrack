BEGIN TRANSACTION;

BEGIN TRY
	-- Insert sample data into JobRole table
	--Begin transaction;
    INSERT INTO JobRole (JOB_TITLE) VALUES 
    ('Administrator'),
    ('Accountant'),
    ('Auditor');

    -- Insert sample data into Account table
    INSERT INTO Account (ACCOUNT_TITLE, ACCOUNT_NUM) VALUES 
    ('HUZAIFAH TARIQ AHMED',   '1015897439573'),
    ('DANIYAL AHMED',   '1022385903479'),
    ('SAMIYA ALI ZAIDI', '1209357984375');

    -- Insert sample data into User table
    INSERT INTO [User] ([USER_NAME], USER_DOB, FK_JOB_ROLE_ID, USER_EMAIL, USER_PASSWORD) VALUES 
    ('John Doe', '1990-01-01', 2, 'john@example.com', 'password123'),
	('Daniyal Zaidi', '1990-01-01', 2, 'daniyal@what.com', 'iAmDaniyal'),
	('Daniyal Cool', '2005-01-01', 2, 'cool@example.com', 'daniyal'),
    ('Jane Smith', '1985-05-12', 3, 'jane@example.com', 'securepass'),
    ('Michael Brown', '1978-07-24', 3, 'michael@example.com', 'mypassword'),
    ('Michael Blue', '1998-07-24', 3, 'm_blue@example.com', 'password');

    -- Insert sample data into Permission table
    INSERT INTO Permission ([PERMISSION_NAME]) VALUES 
    ('Add'),
    ('View'),
    ('Edit'),
    ('Delete');

    -- Insert sample data into JobRolePermission table
    INSERT INTO JobRolePermission (FK_JOB_ROLE_ID, FK_PERMISSION_ID) VALUES 
    (1, 1),  -- Administrator with Add permission
    (1, 2),  -- Administrator with View permission
    (1, 3),  -- Administrator with Edit permission
    (1, 4),  -- Administrator with Delete permission
    (2, 2),  -- Accountant with View permission
    (2, 3),  -- Accountant with Edit permission
    (3, 2);  -- Auditor with View permission

    -- Insert sample data into Category table
    INSERT INTO Category (CATEGORY_NAME) VALUES 
    ('Expense'),
    ('Revenue');

    -- Insert sample data into SubCategory table
    INSERT INTO SubCategory (SUB_CATEGORY_NAME, FK_CATEGORY_ID) VALUES 
    ('Purchase', 1), 
    ('Sales', 2), 
    ('Payment', 1),
	('Receipts', 2);

    -- Insert sample data into ExpenseType table
    INSERT INTO ExpenseType (EXPENSE_TITLE, FK_SUB_CATEGORY_ID) VALUES 
    ('Product Sales', 2),
    ('Office Supplies', 1),
    ('Utilities', 1),
	('Equipment Payment', 3),
	('Service Charges', 2), 
	('Internet Fees', 3),
	('Interest Payment', 3),
	('Dividends Revenue', 4),
	('Marketing Expense', 1);

    -- Insert sample data into PaymentMethod table
    INSERT INTO PaymentMethod (PAYMENT_METHOD_NAME) VALUES 
    ('Credit Card'),
	('Debit Card'),
	('Mobile Payment'),
    ('Wire Transfer'),
	('Pay Order'),
	('Cheque'),
    ('Cash');

    -- Insert sample data into UserAccount table (Bridge Table)
    INSERT INTO UserAccount (FK_USER_ID, FK_ACCOUNT_ID) VALUES 
    (1, 1001), 
    (2, 1002), 
    (3, 1003);

    -- Insert sample data into Transaction table
    INSERT INTO [Transaction] (FK_PAYMENT_METHOD_ID, FK_ACCOUNT_ID, FK_EXPENSE_ID, TRANSACTION_DATE, FK_CREATED_BY, TRANSACTION_AMOUNT, FK_LAST_UPDATED_BY) VALUES 
    (1, 1001, 1, '2024-11-01', 1, 500.00, 1),
    (2, 1002, 2, '2024-11-02', 2, 300.00, 2),
    (3, 1003, 3, '2024-11-03', 3, 200.00, 3);

    -- Insert sample data into ReportLog table
    INSERT INTO ReportLog (REPORT_TYPE, FK_GENERATED_BY, GENERATION_DATE, [START_DATE], END_DATE) VALUES 
    ('Monthly Report', 1, '2024-11-04', '2024-10-01', '2024-10-31'),
    ('Annual Report', 2, '2024-11-05', '2024-01-01', '2024-12-31');

    -- If all inserts succeed, commit the transaction
    COMMIT TRANSACTION;
    PRINT 'Data inserted successfully.';

END TRY
BEGIN CATCH
    -- If there is an error, roll back the transaction
    ROLLBACK TRANSACTION;
    PRINT 'Error occurred. Transaction rolled back.';
    PRINT ERROR_MESSAGE();
END CATCH;