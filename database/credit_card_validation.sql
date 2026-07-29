-- ============================================================
-- CREDIT CARD BALANCE TABLE VALIDATION
-- Purpose: Validate that credit_card_balance.csv has been
-- successfully loaded into PostgreSQL.
-- ============================================================


-- ============================================================
-- 1. Total Rows
-- ============================================================

SELECT COUNT(*) AS total_rows
FROM raw.credit_card_balance;

-- Verified Result:
-- Total Rows: 3,840,312


-- ============================================================
-- 2. Total Columns
-- ============================================================

SELECT COUNT(*) AS total_columns
FROM information_schema.columns
WHERE table_schema='raw'
AND table_name='credit_card_balance';

-- Verified Result:
-- Total Columns: 23


-- ============================================================
-- 3. Unique Previous Credit Accounts
-- ============================================================

SELECT COUNT(DISTINCT "SK_ID_PREV") AS unique_previous_loans
FROM raw.credit_card_balance;

-- Verified Result:
-- Unique Previous Credit Accounts: 104,307


-- ============================================================
-- 4. Unique Applicants
-- ============================================================

SELECT COUNT(DISTINCT "SK_ID_CURR") AS unique_applicants
FROM raw.credit_card_balance;

-- Verified Result:
-- Unique Applicants: 103,558


-- ============================================================
-- 5. Monthly Record Validation
-- ============================================================

SELECT
    COUNT(*) AS total_rows,
    COUNT(DISTINCT ("SK_ID_PREV","MONTHS_BALANCE")) AS unique_monthly_records
FROM raw.credit_card_balance;

-- Verified Result:
-- Total Rows: 3,840,312
-- Unique Monthly Records: 3,840,312


-- ============================================================
-- Validation Summary
-- ============================================================
-- ✔ Total Rows                     : 3,840,312
-- ✔ Total Columns                  : 23
-- ✔ Unique Previous Credit Accounts: 104,307
-- ✔ Unique Applicants              : 103,558
-- ✔ Monthly Records Verified       : 3,840,312
--
-- Notes:
-- • Each (SK_ID_PREV, MONTHS_BALANCE) combination is unique.
-- • SK_ID_PREV repeats because each credit card account has
--   multiple monthly records.
-- • SK_ID_CURR repeats because customers may own multiple
--   credit card accounts.
--
