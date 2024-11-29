DECLARE @StartDate DATE = '2024-11-01';
DECLARE @EndDate DATE = '2024-11-30';

-- Income Statement Query
SELECT
    -- Net Sales (Revenue from sales transactions)
    SUM(CASE 
            WHEN sc.FK_CATEGORY_ID = 4 AND et.FK_SUB_CATEGORY_ID = 6 THEN t.TRANSACTION_AMOUNT -- Sales Revenue
        END) AS NetSales,

    -- Cost of Sales
    SUM(CASE 
            WHEN sc.FK_CATEGORY_ID = 3 AND et.FK_SUB_CATEGORY_ID = 5 THEN -t.TRANSACTION_AMOUNT -- Cost of Goods Sold (COGS)
        END) AS CostOfSales,

    -- Gross Profit
    SUM(CASE 
            WHEN sc.FK_CATEGORY_ID = 4 AND et.FK_SUB_CATEGORY_ID = 6 THEN t.TRANSACTION_AMOUNT -- Sales Revenue
            WHEN sc.FK_CATEGORY_ID = 3 AND et.FK_SUB_CATEGORY_ID = 5 THEN -t.TRANSACTION_AMOUNT -- Subtract COGS
        END) AS GrossProfit,

    -- Selling and Operating Expenses
    SUM(CASE 
            WHEN sc.FK_CATEGORY_ID = 3 AND et.FK_SUB_CATEGORY_ID IN (8, 9) THEN -t.TRANSACTION_AMOUNT -- Selling and Operating Expenses
        END) AS SellingOperatingExpenses,

    -- General and Administrative Expenses
    SUM(CASE 
            WHEN sc.FK_CATEGORY_ID = 3 AND et.FK_SUB_CATEGORY_ID = 10 THEN -t.TRANSACTION_AMOUNT -- General/Admin Expenses
        END) AS GeneralAdminExpenses,

    -- Total Operating Expenses
    SUM(CASE 
            WHEN sc.FK_CATEGORY_ID = 3 AND et.FK_SUB_CATEGORY_ID IN (8, 9, 10) THEN -t.TRANSACTION_AMOUNT -- All Operating Expenses
        END) AS TotalOperatingExpenses,

    -- Other Income
    SUM(CASE 
            WHEN sc.FK_CATEGORY_ID = 4 AND et.FK_SUB_CATEGORY_ID = 11 THEN t.TRANSACTION_AMOUNT -- Other Income (e.g., non-operational revenue)
        END) AS OtherIncome,

    -- Income Before Taxes
    SUM(CASE 
            WHEN sc.FK_CATEGORY_ID = 4 AND et.FK_SUB_CATEGORY_ID IN (6, 11) THEN t.TRANSACTION_AMOUNT -- Net Sales + Other Income
            WHEN sc.FK_CATEGORY_ID = 3 AND et.FK_SUB_CATEGORY_ID IN (5, 8, 9, 10) THEN -t.TRANSACTION_AMOUNT -- COGS + Operating Expenses
        END) AS IncomeBeforeTaxes,

    -- Income Tax Expense
    SUM(CASE 
            WHEN sc.FK_CATEGORY_ID = 3 AND et.FK_SUB_CATEGORY_ID = 12 THEN -t.TRANSACTION_AMOUNT -- Income Taxes
        END) AS IncomeTaxExpense,

    -- Net Income
    SUM(CASE 
            WHEN sc.FK_CATEGORY_ID = 4 AND et.FK_SUB_CATEGORY_ID IN (6, 11) THEN t.TRANSACTION_AMOUNT -- Net Sales + Other Income
            WHEN sc.FK_CATEGORY_ID = 3 AND et.FK_SUB_CATEGORY_ID IN (5, 8, 9, 10, 12) THEN -t.TRANSACTION_AMOUNT -- Subtract Expenses (COGS, Operating, Taxes)
        END) AS NetIncome
FROM 
    [Transaction] t
INNER JOIN [ExpenseType] et ON t.FK_EXPENSE_ID = et.EXPENSE_ID
INNER JOIN [SubCategory] sc ON et.FK_SUB_CATEGORY_ID = sc.SUB_CATEGORY_ID
WHERE 
    t.TRANSACTION_DATE BETWEEN @StartDate AND @EndDate;

SELECT * FROM SubCategory

SELECT EXPENSE_ID, EXPENSE_TITLE, SC.SUB_CATEGORY_NAME, C.CATEGORY_NAME FROM ExpenseType
INNER JOIN SubCategory SC ON SC.SUB_CATEGORY_ID = FK_SUB_CATEGORY_ID
INNER JOIN Category C ON SC.FK_CATEGORY_ID = C.CATEGORY_ID



SELECT TRANSACTION_AMOUNT, E.EXPENSE_TITLE, SC.SUB_CATEGORY_NAME FROM [Transaction] T
INNER JOIN ExpenseType E ON E.EXPENSE_ID = T.FK_EXPENSE_ID
INNER JOIN [SubCategory] SC ON SC.SUB_CATEGORY_ID = E.FK_SUB_CATEGORY_ID

-- INCOME STATEMENT QUERY

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

SELECT * FROM [Transaction]T


-- GPT GENERATED QUERY FOR INCOME STATEMENT:
SELECT 

-- Revenues
SUM(CASE 
    WHEN SC.SUB_CATEGORY_ID = 6 THEN T.TRANSACTION_AMOUNT -- Total Sales Revenue
    WHEN E.EXPENSE_ID = 11 THEN T.TRANSACTION_AMOUNT -- Product Sales
    WHEN E.EXPENSE_ID = 15 THEN T.TRANSACTION_AMOUNT -- Service Charges
END) AS 'Total Revenue',

-- Direct Costs / COGS
SUM(CASE 
    WHEN SC.SUB_CATEGORY_ID = 5 THEN T.TRANSACTION_AMOUNT -- Total Purchase Expense
END) AS 'Total Purchase Expense',

-- Operating Expenses
SUM(CASE 
    WHEN E.EXPENSE_ID IN (12, 13) THEN T.TRANSACTION_AMOUNT -- Office Supplies & Utilities
    WHEN E.EXPENSE_ID = 14 THEN T.TRANSACTION_AMOUNT -- Equipment Payment
    WHEN E.EXPENSE_ID = 16 THEN T.TRANSACTION_AMOUNT -- Internet Fees
    WHEN E.EXPENSE_ID = 19 THEN T.TRANSACTION_AMOUNT -- Marketing Expense
END) AS 'Total Operating Expense',

-- Other Income/Expense
SUM(CASE 
    WHEN E.EXPENSE_ID = 18 THEN T.TRANSACTION_AMOUNT -- Dividends Revenue
    --WHEN SC.FK_CATEGORY_ID = 8 THEN T.TRANSACTION_AMOUNT -- Receipts Revenue
    WHEN E.EXPENSE_ID = 17 THEN -T.TRANSACTION_AMOUNT -- Interest Payment (Negative)
END) AS 'Other Income/Expense',

-- Gross Revenue
SUM(CASE 
    WHEN SC.FK_CATEGORY_ID = 4 THEN T.TRANSACTION_AMOUNT -- Revenue
    WHEN SC.FK_CATEGORY_ID = 3 THEN -T.TRANSACTION_AMOUNT -- Expense
END) AS 'Gross Revenue'

FROM [Transaction] T
INNER JOIN ExpenseType E ON E.EXPENSE_ID = T.FK_EXPENSE_ID
INNER JOIN [SubCategory] SC ON SC.SUB_CATEGORY_ID = E.FK_SUB_CATEGORY_ID
--WHERE T.TRANSACTION_DATE BETWEEN 'start_date' AND 'end_date';
