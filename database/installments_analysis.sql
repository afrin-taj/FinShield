-- ============================================================
-- INSTALLMENTS PAYMENTS BUSINESS ANALYSIS
-- Purpose: Analyze customer repayment behavior and payment trends.
-- ============================================================


-- ============================================================
-- 1. Total Amount Due
-- ============================================================

SELECT
    ROUND(SUM("AMT_INSTALMENT")::numeric,2) AS total_amount_due
FROM raw.installments_payments;

-- Verified Result:
-- Total Amount Due: 231,984,426,998.63


-- ============================================================
-- 2. Total Amount Paid
-- ============================================================

SELECT
    ROUND(SUM("AMT_PAYMENT")::numeric,2) AS total_amount_paid
FROM raw.installments_payments;

-- Verified Result:
-- Total Amount Paid: 234,482,862,799.57


-- ============================================================
-- 3. Average Installment Amount
-- ============================================================

SELECT
    ROUND(AVG("AMT_INSTALMENT")::numeric,2) AS avg_installment
FROM raw.installments_payments;

-- Verified Result:
-- Average Installment Amount: 17,050.91


-- ============================================================
-- 4. Average Payment Amount
-- ============================================================

SELECT
    ROUND(AVG("AMT_PAYMENT")::numeric,2) AS avg_payment
FROM raw.installments_payments;

-- Verified Result:
-- Average Payment Amount: 17,238.22


-- ============================================================
-- 5. Late Payments
-- ============================================================

SELECT
    COUNT(*) AS late_payments
FROM raw.installments_payments
WHERE "DAYS_ENTRY_PAYMENT" > "DAYS_INSTALMENT";

-- Verified Result:
-- Late Payments: 1,146,669


-- ============================================================
-- 6. Early / On-Time Payments
-- ============================================================

SELECT
    COUNT(*) AS early_or_ontime_payments
FROM raw.installments_payments
WHERE "DAYS_ENTRY_PAYMENT" <= "DAYS_INSTALMENT";

-- Verified Result:
-- Early / On-Time Payments: 12,455,827


-- ============================================================
-- 7. Average Payment Delay
-- ============================================================

SELECT
    ROUND(
        AVG("DAYS_ENTRY_PAYMENT" - "DAYS_INSTALMENT")::numeric,
        2
    ) AS avg_delay_days
FROM raw.installments_payments
WHERE "DAYS_ENTRY_PAYMENT" IS NOT NULL;

-- Verified Result:
-- Average Delay: -8.79 Days
-- Interpretation:
-- Customers pay approximately 9 days before the due date on average.


-- ============================================================
-- 8. Customers with Highest Average Delay
-- ============================================================

SELECT
    "SK_ID_CURR",
    ROUND(
        AVG("DAYS_ENTRY_PAYMENT" - "DAYS_INSTALMENT")::numeric,
        2
    ) AS avg_delay
FROM raw.installments_payments
WHERE "DAYS_ENTRY_PAYMENT" IS NOT NULL
GROUP BY "SK_ID_CURR"
ORDER BY avg_delay DESC
LIMIT 10;

-- Verified Result:
-- 184984 : 1884.20 Days
-- 230218 : 1406.00 Days
-- 225340 : 1378.50 Days
-- 210216 : 950.00 Days
-- 164168 : 945.33 Days
-- 164255 : 762.00 Days
-- 168241 : 715.00 Days
-- 403582 : 688.50 Days
-- 319829 : 688.50 Days
-- 156137 : 565.80 Days


-- ============================================================
-- 9. Fully Paid Installments
-- ============================================================

SELECT
    COUNT(*) AS fully_paid
FROM raw.installments_payments
WHERE "AMT_PAYMENT" >= "AMT_INSTALMENT";

-- Verified Result:
-- Fully Paid Installments: 12,307,003


-- ============================================================
-- 10. Underpaid Installments
-- ============================================================

SELECT
    COUNT(*) AS underpaid
FROM raw.installments_payments
WHERE "AMT_PAYMENT" < "AMT_INSTALMENT";

-- Verified Result:
-- Underpaid Installments: 1,295,493


-- ============================================================
-- 11. Average Payment Completion Percentage
-- ============================================================

SELECT
    ROUND(
        AVG(
            ("AMT_PAYMENT" / NULLIF("AMT_INSTALMENT",0))*100
        )::numeric,
        2
    ) AS avg_payment_completion_percent
FROM raw.installments_payments
WHERE "AMT_PAYMENT" IS NOT NULL;

-- Verified Result:
-- Average Payment Completion: 127.83%


-- ============================================================
-- 12. Customers with Highest Total Payments
-- ============================================================

SELECT
    "SK_ID_CURR",
    ROUND(SUM("AMT_PAYMENT")::numeric,2) AS total_paid
FROM raw.installments_payments
GROUP BY "SK_ID_CURR"
ORDER BY total_paid DESC
LIMIT 10;

-- Verified Result:
-- 405063 : null
-- 329430 : null
-- 389262 : null
-- 263534 : null
-- 151950 : null
-- 153598 : null
-- 230272 : null
-- 338747 : null
-- 220039 : null
-- 149858 : 32,689,281.51