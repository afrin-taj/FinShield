-- ============================================================
-- PREVIOUS APPLICATION BUSINESS ANALYSIS
-- Purpose: Analyze historical loan application trends and
-- customer behavior using previous_application data.
-- ============================================================


-- ============================================================
-- 1. Previous Application Status Distribution
-- ============================================================

SELECT
    "NAME_CONTRACT_STATUS",
    COUNT(*) AS total_applications,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (),2) AS percentage
FROM raw.previous_application
GROUP BY "NAME_CONTRACT_STATUS"
ORDER BY total_applications DESC;

-- Verified Result:
-- Approved     : 1,036,781 (62.07%)
-- Canceled     :   316,319 (18.94%)
-- Refused      :   290,678 (17.40%)
-- Unused offer :    26,436 (1.58%)


-- ============================================================
-- 2. Loan Type Distribution
-- ============================================================

SELECT
    "NAME_CONTRACT_TYPE",
    COUNT(*) AS total_loans
FROM raw.previous_application
GROUP BY "NAME_CONTRACT_TYPE"
ORDER BY total_loans DESC;

-- Verified Result:
-- Cash loans       : 747,553
-- Consumer loans   : 729,151
-- Revolving loans  : 193,164
-- XNA              : 346


-- ============================================================
-- 3. Average Loan Amount Requested
-- ============================================================

SELECT
ROUND(AVG("AMT_APPLICATION")::numeric,2) AS avg_application_amount
FROM raw.previous_application;

-- Verified Result:
-- Average Requested Amount: 175,233.86


-- ============================================================
-- 4. Average Credit Approved
-- ============================================================

SELECT
ROUND(AVG("AMT_CREDIT")::numeric,2) AS avg_credit_amount
FROM raw.previous_application;

-- Verified Result:
-- Average Credit Amount: 196,114.02


-- ============================================================
-- 5. Average Previous Applications per Customer
-- ============================================================

SELECT
ROUND(AVG(application_count),2) AS avg_previous_applications
FROM
(
SELECT
"SK_ID_CURR",
COUNT(*) AS application_count
FROM raw.previous_application
GROUP BY "SK_ID_CURR"
) t;

-- Verified Result:
-- Average Previous Applications per Customer: 4.93


-- ============================================================
-- 6. Top 10 Customers by Number of Applications
-- ============================================================

SELECT
"SK_ID_CURR",
COUNT(*) AS total_previous_applications
FROM raw.previous_application
GROUP BY "SK_ID_CURR"
ORDER BY total_previous_applications DESC
LIMIT 10;

-- Verified Result:
-- 187868 : 77
-- 265681 : 73
-- 173680 : 72
-- 242412 : 68
-- 206783 : 67
-- 156367 : 66
-- 382179 : 64
-- 389950 : 64
-- 198355 : 63
-- 345161 : 62


-- ============================================================
-- 7. Average Requested Amount by Loan Type
-- ============================================================

SELECT
"NAME_CONTRACT_TYPE",
ROUND(AVG("AMT_APPLICATION")::numeric,2) AS avg_requested_amount
FROM raw.previous_application
GROUP BY "NAME_CONTRACT_TYPE"
ORDER BY avg_requested_amount DESC;

-- Verified Result:
-- Cash loans      : 274,760.43
-- Revolving loans : 97,816.24
-- Consumer loans  : 93,787.83
-- XNA             : 0.00


-- ============================================================
-- 8. Overall Approval Rate
-- ============================================================

SELECT
ROUND(
SUM(
CASE
WHEN "NAME_CONTRACT_STATUS"='Approved'
THEN 1 ELSE 0
END
)*100.0/COUNT(*),2) AS approval_rate
FROM raw.previous_application;

-- Verified Result:
-- Approval Rate: 62.07%


-- ============================================================
-- 9. Overall Refusal Rate
-- ============================================================

SELECT
ROUND(
SUM(
CASE
WHEN "NAME_CONTRACT_STATUS"='Refused'
THEN 1 ELSE 0
END
)*100.0/COUNT(*),2) AS refusal_rate
FROM raw.previous_application;

-- Verified Result:
-- Refusal Rate: 17.40%


-- ============================================================
-- 10. Average Credit Amount by Application Status
-- ============================================================

SELECT
"NAME_CONTRACT_STATUS",
ROUND(AVG("AMT_CREDIT"),2) AS avg_credit
FROM raw.previous_application
GROUP BY "NAME_CONTRACT_STATUS"
ORDER BY avg_credit DESC;

-- Verified Result:
-- Refused      : 371,689.84
-- Approved     : 202,564.18
-- Unused offer : 69,783.99
-- Canceled     : 24,187.06


-- ============================================================
-- Business Insights
-- ============================================================
-- • Approximately 62% of previous applications were approved,
--   indicating a relatively high historical approval rate.
--
-- • Cash Loans are the most frequently requested loan product,
--   closely followed by Consumer Loans.
--
-- • On average, customers requested loans worth 175,233.86,
--   while the average approved credit amount was 196,114.02.
--
-- • Each customer submitted an average of 4.93 previous
--   applications, suggesting many repeat applicants.
--
-- • Some customers applied more than 70 times, indicating
--   repeated borrowing or multiple financing attempts.
--
-- • Refused applications have the highest average requested
--   credit amount, suggesting that larger loan requests may
--   face stricter approval criteria.