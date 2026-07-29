-- ============================================================
-- POS CASH BALANCE BUSINESS ANALYSIS
-- Purpose: Analyze customer loan repayment behavior,
-- contract status, and delinquency patterns.
-- ============================================================


-- ============================================================
-- 1. Contract Status Distribution
-- ============================================================

SELECT
    "NAME_CONTRACT_STATUS",
    COUNT(*) AS total_records
FROM raw.pos_cash_balance
GROUP BY "NAME_CONTRACT_STATUS"
ORDER BY total_records DESC;

-- Verified Result:
-- Active                : 7,155,113
-- Completed             :   525,124
-- Signed                :    60,101
-- Returned to the store :     3,815
-- Approved              :     3,669
-- Demand                :     2,047
-- Amortized debt        :       122
-- Canceled              :         7
-- XNA                   :         2


-- ============================================================
-- 2. Active Contract Records
-- ============================================================

SELECT COUNT(*) AS active_contracts
FROM raw.pos_cash_balance
WHERE "NAME_CONTRACT_STATUS"='Active';

-- Verified Result:
-- Active Contracts: 7,155,113


-- ============================================================
-- 3. Completed Contract Records
-- ============================================================

SELECT COUNT(*) AS completed_contracts
FROM raw.pos_cash_balance
WHERE "NAME_CONTRACT_STATUS"='Completed';

-- Verified Result:
-- Completed Contracts: 525,124


-- ============================================================
-- 4. Average Total Installments
-- ============================================================

SELECT ROUND(AVG("CNT_INSTALMENT")::numeric ,2)
FROM raw.pos_cash_balance;

-- Verified Result:
-- Average Installments: 17.73


-- ============================================================
-- 5. Average Remaining Installments
-- ============================================================

SELECT ROUND(AVG("CNT_INSTALMENT_FUTURE")::numeric ,2)
FROM raw.pos_cash_balance;

-- Verified Result:
-- Average Remaining Installments: 11.28


-- ============================================================
-- 6. Total Overdue Days
-- ============================================================

SELECT SUM("SK_DPD")
FROM raw.pos_cash_balance;

-- Verified Result:
-- Total Overdue Days: 39,530,590


-- ============================================================
-- 7. Total Default Overdue Days
-- ============================================================

SELECT SUM("SK_DPD_DEF")
FROM raw.pos_cash_balance;

-- Verified Result:
-- Total Default Overdue Days: 1,823,412


-- ============================================================
-- 8. Average Overdue Days
-- ============================================================

SELECT ROUND(AVG("SK_DPD")::numeric,2)
FROM raw.pos_cash_balance;

-- Verified Result:
-- Average Overdue Days: 5.10


-- ============================================================
-- 9. Customers with Highest Overdue Days
-- ============================================================

SELECT
    "SK_ID_CURR",
    SUM("SK_DPD") AS total_overdue
FROM raw.pos_cash_balance
GROUP BY "SK_ID_CURR"
ORDER BY total_overdue DESC
LIMIT 10;

-- Verified Result:
-- 450875 : 170162
-- 402388 : 159744
-- 240380 : 151130
-- 376955 : 150450
-- 282285 : 128921
-- 270342 : 119202
-- 234153 : 119189
-- 153194 : 116359
-- 354104 : 116348
-- 372137 : 115415


-- ============================================================
-- 10. Monthly Balance Range
-- ============================================================

SELECT
    MIN("MONTHS_BALANCE"),
    MAX("MONTHS_BALANCE")
FROM raw.pos_cash_balance;

-- Verified Result:
-- Earliest Month : -96
-- Latest Month   : -1


-- ============================================================
-- 11. Loans with Highest Remaining Installments
-- ============================================================

SELECT
    "SK_ID_PREV",
    MAX("CNT_INSTALMENT_FUTURE") AS remaining_installments
FROM raw.pos_cash_balance
WHERE "CNT_INSTALMENT_FUTURE" IS NOT NULL
GROUP BY "SK_ID_PREV"
ORDER BY remaining_installments DESC
LIMIT 10;

-- Verified Result:
-- SK_ID_PREV : Remaining Installments
-- 1411674 : 85
-- 2416673 : 84
-- 1257406 : 72
-- 1118666 : 72
-- 1159544 : 72
-- 1210170 : 72
-- 1276203 : 72
-- 1044486 : 72
-- 1093337 : 72
-- 1280839 : 72

-- ============================================================
-- 12. Average Overdue Days by Contract Status
-- ============================================================

SELECT
    "NAME_CONTRACT_STATUS",
    ROUND(AVG("SK_DPD"),2) AS avg_overdue_days
FROM raw.pos_cash_balance
GROUP BY "NAME_CONTRACT_STATUS"
ORDER BY avg_overdue_days DESC;

-- Verified Result:
-- Amortized debt        : 1942.25
-- Demand                : 505.04
-- Completed             : 10.05
-- Active                : 4.61
-- Returned to the store : 0.01
-- Signed                : 0.01
-- Canceled              : 0.00
-- Approved              : 0.00
-- XNA                   : 0.00

-- ============================================================
-- Business Insights
-- ============================================================
-- 1. Over 92% of the monthly records belong to Active contracts,
--    indicating that most POS loans are still under repayment.
--
-- 2. Customers have an average of 17.73 scheduled installments,
--    with approximately 11.28 installments remaining, showing
--    that many loans are still active.
--
-- 3. The dataset records over 39.5 million overdue days,
--    highlighting repayment delays as an important indicator
--    of customer credit behavior.
--
-- 4. The average overdue period is 5.10 days, suggesting that
--    most customers pay close to the due date while a smaller
--    group experiences significant delays.
--
-- 5. Contract statuses such as 'Amortized debt' and 'Demand'
--    show the highest average overdue days, making them useful
--    indicators of elevated credit risk.
--
-- 6. The repayment history spans 96 months, providing sufficient
--    historical information for future feature engineering and
--    predictive credit risk modeling.