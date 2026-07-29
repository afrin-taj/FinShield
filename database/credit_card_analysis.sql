-- ============================================================
-- CREDIT CARD BALANCE BUSINESS ANALYSIS
-- Purpose: Analyze customer credit card usage, balances,
-- payments, and delinquency patterns.
-- ============================================================


-- ============================================================
-- 1. Contract Status Distribution
-- ============================================================

SELECT
    "NAME_CONTRACT_STATUS",
    COUNT(*) AS total_records
FROM raw.credit_card_balance
GROUP BY "NAME_CONTRACT_STATUS"
ORDER BY total_records DESC;

-- Verified Result:
-- Active         : 7,396,872
-- Completed      :   257,836
-- Signed         :    22,116
-- Demand         :     2,730
-- Sent proposal  :     1,026
-- Refused        :        34
-- Approved       :        10


-- ============================================================
-- 2. Total Outstanding Balance
-- ============================================================

SELECT ROUND(SUM("AMT_BALANCE")::numeric,2) AS total_balance
FROM raw.credit_card_balance;

-- Verified Result:
-- Total Outstanding Balance: 447,781,571,707.95


-- ============================================================
-- 3. Average Outstanding Balance
-- ============================================================

SELECT ROUND(AVG("AMT_BALANCE")::numeric,2) AS avg_balance
FROM raw.credit_card_balance;

-- Verified Result:
-- Average Outstanding Balance: 58,300.16


-- ============================================================
-- 4. Total Credit Limit
-- ============================================================

SELECT ROUND(SUM("AMT_CREDIT_LIMIT_ACTUAL")::numeric,2) AS total_credit_limit
FROM raw.credit_card_balance;

-- Verified Result:
-- Total Credit Limit: 1,181,341,089,000.00


-- ============================================================
-- 5. Average Credit Limit
-- ============================================================

SELECT ROUND(AVG("AMT_CREDIT_LIMIT_ACTUAL")::numeric,2) AS avg_credit_limit
FROM raw.credit_card_balance;

-- Verified Result:
-- Average Credit Limit: 153,807.96


-- ============================================================
-- 6. Total Customer Payments
-- ============================================================

SELECT ROUND(SUM("AMT_PAYMENT_TOTAL_CURRENT")::numeric,2) AS total_payments
FROM raw.credit_card_balance;

-- Verified Result:
-- Total Customer Payments: 58,287,155,205.69


-- ============================================================
-- 7. Average Customer Payments
-- ============================================================

SELECT ROUND(AVG("AMT_PAYMENT_TOTAL_CURRENT")::numeric,2) AS avg_payment
FROM raw.credit_card_balance;

-- Verified Result:
-- Average Customer Payment: 7,588.86


-- ============================================================
-- 8. Total ATM Withdrawals
-- ============================================================

SELECT ROUND(SUM("AMT_DRAWINGS_ATM_CURRENT")::numeric,2) AS total_atm_withdrawals
FROM raw.credit_card_balance;

-- Verified Result:
-- Total ATM Withdrawals: 36,846,901,034.55


-- ============================================================
-- 9. Total POS Purchase Amount
-- ============================================================

SELECT ROUND(SUM("AMT_DRAWINGS_POS_CURRENT")::numeric,2) AS total_pos_purchases
FROM raw.credit_card_balance;

-- Verified Result:
-- Total POS Purchases: 18,350,159,013.09


-- ============================================================
-- 10. Top Customers by Outstanding Balance
-- ============================================================

SELECT
    "SK_ID_CURR",
    ROUND(SUM("AMT_BALANCE"),2) AS outstanding_balance
FROM raw.credit_card_balance
GROUP BY "SK_ID_CURR"
ORDER BY outstanding_balance DESC
LIMIT 10;

-- Verified Result:
-- 155492 : 59,960,968.83
-- 299213 : 58,984,232.49
-- 172610 : 58,421,871.99
-- 166833 : 53,616,326.13
-- 363382 : 50,346,679.23
-- 302113 : 50,135,562.54
-- 432295 : 49,743,586.62
-- 200699 : 49,694,533.11
-- 284974 : 49,488,796.35
-- 195075 : 49,351,965.84


-- ============================================================
-- 11. Top Customers by Credit Limit
-- ============================================================

SELECT
    "SK_ID_CURR",
    MAX("AMT_CREDIT_LIMIT_ACTUAL") AS credit_limit
FROM raw.credit_card_balance
GROUP BY "SK_ID_CURR"
ORDER BY credit_limit DESC
LIMIT 10;

-- Verified Result:
-- 353597 : 1,350,000
-- 272499 : 1,350,000
-- 338123 : 1,350,000
-- 154897 : 1,350,000
-- 423213 : 1,350,000
-- 291602 : 1,350,000
-- 135194 : 1,350,000
-- 156500 : 1,350,000
-- 303663 : 1,350,000
-- 256351 : 1,350,000


-- ============================================================
-- 12. Average Overdue Days by Contract Status
-- ============================================================

SELECT
    "NAME_CONTRACT_STATUS",
    ROUND(AVG("SK_DPD"),2) AS avg_overdue_days
FROM raw.credit_card_balance
GROUP BY "NAME_CONTRACT_STATUS"
ORDER BY avg_overdue_days DESC;

-- Verified Result:
-- Demand         : 747.05
-- Active         : 9.36
-- Signed         : 0.73
-- Completed      : 0.05
-- Approved       : 0.00
-- Refused        : 0.00
-- Sent proposal  : 0.00


-- ============================================================
-- Business Insights
-- ============================================================
-- 1. More than 96% of credit card records belong to Active
--    contracts, indicating that most credit card accounts are
--    currently in use.
--
-- 2. The total outstanding balance exceeds 447.78 billion,
--    reflecting significant credit exposure across customers.
--
-- 3. The average customer maintains an outstanding balance of
--    approximately 58,300, while the average credit limit is
--    about 153,808.
--
-- 4. Customers have made total payments exceeding 58.29 billion,
--    demonstrating substantial repayment activity.
--
-- 5. ATM withdrawals (36.85 billion) are considerably higher
--    than POS purchase withdrawals (18.35 billion), indicating
--    that cash advances represent a significant portion of
--    credit card usage.
--
-- 6. Customers under the 'Demand' contract status have the
--    highest average overdue period (747.05 days), making this
--    status a strong indicator of elevated credit risk.