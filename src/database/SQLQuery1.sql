WITH CategorizedTransactions AS (
    SELECT 
        T.TRANSACTION_DATE,
        T.TRANSACTION_AMOUNT,
        CASE 
            WHEN SC.FK_CATEGORY_ID = 1 THEN 'Operating'  -- Example: Operating category ID
            WHEN SC.FK_CATEGORY_ID = 2 THEN 'Investing' -- Example: Investing category ID
            WHEN SC.FK_CATEGORY_ID = 3 THEN 'Financing' -- Example: Financing category ID
            ELSE 'Uncategorized'
        END AS CashFlowType
    FROM 
        [dbo].[Transaction] T
    LEFT JOIN 
        [dbo].[ExpenseType] ET ON T.FK_EXPENSE_ID = ET.EXPENSE_ID
    LEFT JOIN 
        [dbo].[SubCategory] SC ON ET.FK_SUB_CATEGORY_ID = SC.SUB_CATEGORY_ID
)
SELECT 
    CashFlowType,
    SUM(CASE WHEN TRANSACTION_AMOUNT > 0 THEN TRANSACTION_AMOUNT ELSE 0 END) AS CashInflows,
    SUM(CASE WHEN TRANSACTION_AMOUNT < 0 THEN TRANSACTION_AMOUNT ELSE 0 END) AS CashOutflows,
    SUM(TRANSACTION_AMOUNT) AS NetCashFlow
FROM 
    CategorizedTransactions
GROUP BY 
    CashFlowType
ORDER BY 
    CashFlowType;

SELECT * FROM SubCategory

DECLARE @StartDate DATE = '2024-11-01';
DECLARE @EndDate DATE = '2024-11-30';

-- Cash Flow Statement Query
SELECT
    -- Net Earnings
    SUM(CASE 
            WHEN sc.FK_CATEGORY_ID = 4 THEN t.TRANSACTION_AMOUNT -- Revenue
            WHEN sc.FK_CATEGORY_ID = 3 THEN -t.TRANSACTION_AMOUNT -- Expenses
        END) AS NetEarnings,
    
    -- Net Cash from Operations
    SUM(CASE 
            WHEN et.FK_SUB_CATEGORY_ID IN (6, 5) THEN -- Sales & Purchases
                CASE 
                    WHEN sc.FK_CATEGORY_ID = 4 THEN t.TRANSACTION_AMOUNT -- Revenue from sales
                    WHEN sc.FK_CATEGORY_ID = 3 THEN -t.TRANSACTION_AMOUNT -- Expense from purchases
                END
        END) AS NetCashFromOperations,
    
    -- Net Cash from Financing
    SUM(CASE 
            WHEN et.FK_SUB_CATEGORY_ID = 7 THEN -- Financing activities like Interest or Dividends
                CASE 
                    WHEN et.EXPENSE_ID IN (17, 18) THEN t.TRANSACTION_AMOUNT -- Dividends and Interest
                    ELSE -t.TRANSACTION_AMOUNT -- Other financing expenses
                END
        END) AS NetCashFromFinancing,
    
    -- Net Cash from Investing
    SUM(CASE 
            WHEN et.FK_SUB_CATEGORY_ID = 7 AND et.EXPENSE_ID = 14 THEN -- Equipment Payment as an investment activity
                -t.TRANSACTION_AMOUNT
        END) AS NetCashFromInvesting,
    
    -- Total Net Cash Flow
    SUM(CASE 
            WHEN sc.FK_CATEGORY_ID = 4 THEN t.TRANSACTION_AMOUNT -- All Revenues
            WHEN sc.FK_CATEGORY_ID = 3 THEN -t.TRANSACTION_AMOUNT -- All Expenses
        END) AS TotalNetCashFlow
FROM 
    [Transaction] t
INNER JOIN [ExpenseType] et ON t.FK_EXPENSE_ID = et.EXPENSE_ID
INNER JOIN [SubCategory] sc ON et.FK_SUB_CATEGORY_ID = sc.SUB_CATEGORY_ID
WHERE 
    t.TRANSACTION_DATE BETWEEN @StartDate AND @EndDate;

SELECT * FROM [Transaction]