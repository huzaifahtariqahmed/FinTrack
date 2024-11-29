SELECT 

SUM(CASE 
    WHEN E.EXPENSE_ID = 15 THEN T.TRANSACTION_AMOUNT -- Service Charges
END) AS 'Service Charges',

SUM(CASE 
    WHEN E.EXPENSE_ID = 11 THEN T.TRANSACTION_AMOUNT -- Product Sales
END) AS 'Product Sales',

SUM(CASE 
    WHEN sc.SUB_CATEGORY_ID = 6 THEN t.TRANSACTION_AMOUNT -- Total Sales Revenue
END) AS 'Total Sales Revenue',

SUM(CASE 
    WHEN E.EXPENSE_ID = 12 THEN T.TRANSACTION_AMOUNT -- Office Supplies
END) AS 'Office Supplies',

SUM(CASE 
    WHEN E.EXPENSE_ID = 13 THEN T.TRANSACTION_AMOUNT -- Utilities
END) AS 'Utilities',

SUM(CASE 
    WHEN E.EXPENSE_ID = 19 THEN T.TRANSACTION_AMOUNT -- Marketing Expense
END) AS 'Marketing Expense',

SUM(CASE 
    WHEN sc.SUB_CATEGORY_ID = 5 THEN t.TRANSACTION_AMOUNT -- Total Purchase Expense
END) AS 'Total Purchase Expense',

SUM(CASE 
    WHEN E.EXPENSE_ID = 14 THEN T.TRANSACTION_AMOUNT -- Equipment Payment
END) AS 'Equipment Payment Expense',

SUM(CASE 
    WHEN E.EXPENSE_ID = 16 THEN T.TRANSACTION_AMOUNT -- Internet Fees
END) AS 'Internet Fees',

SUM(CASE 
    WHEN E.EXPENSE_ID = 17 THEN T.TRANSACTION_AMOUNT -- Internet Payment
END) AS 'Interest Payment',

SUM(CASE 
    WHEN sc.SUB_CATEGORY_ID = 7 THEN t.TRANSACTION_AMOUNT -- Total Purchase Expense
END) AS 'Payment Expense',

SUM(CASE 
    WHEN E.EXPENSE_ID = 18 THEN T.TRANSACTION_AMOUNT -- Dividends Revenue
END) AS 'Dividends Revenue',

SUM(CASE 
    WHEN sc.FK_CATEGORY_ID = 8 THEN t.TRANSACTION_AMOUNT -- Receipts Revenue
END) AS 'Receipts Revenue',

SUM(CASE 
    WHEN sc.FK_CATEGORY_ID = 4 THEN t.TRANSACTION_AMOUNT -- Total Revenue
END) AS 'Revenue',

SUM(CASE 
    WHEN sc.FK_CATEGORY_ID = 4 THEN t.TRANSACTION_AMOUNT -- Revenue
    WHEN sc.FK_CATEGORY_ID = 3 THEN -t.TRANSACTION_AMOUNT -- Expense 
END) AS 'Gross Revenue'

FROM [Transaction] T
INNER JOIN ExpenseType E ON E.EXPENSE_ID = T.FK_EXPENSE_ID
INNER JOIN [SubCategory] SC ON SC.SUB_CATEGORY_ID = E.FK_SUB_CATEGORY_ID
WHERE T.TRANSACTION_DATE BETWEEN 'start_date' AND 'end_date';