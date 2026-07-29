-- ============================================================
-- BUREAU BALANCE TABLE VALIDATION
-- Purpose: Validate that bureau_balance.csv has been
-- successfully loaded into PostgreSQL.
-- ============================================================


-- ============================================================
-- 1. Total Rows
-- ============================================================

SELECT COUNT(*) AS total_rows
FROM raw.bureau_balance;

-- Verified Result:
-- Total Rows: 27,299,925


-- ============================================================
-- 2. Total Columns
-- ============================================================

SELECT COUNT(*) AS total_columns
FROM information_schema.columns
WHERE table_schema = 'raw'
AND table_name = 'bureau_balance';

-- Verified Result:
-- Total Columns: 3


-- ============================================================
-- 3. Unique Bureau Accounts
-- ============================================================

SELECT COUNT(DISTINCT "SK_ID_BUREAU") AS unique_bureau_accounts
FROM raw.bureau_balance;

-- Verified Result:
-- Unique Bureau Accounts: 817,395


-- ============================================================
-- 4. Monthly Record Validation
-- ============================================================

SELECT
    COUNT(*) AS total_rows,
    COUNT(DISTINCT ("SK_ID_BUREAU","MONTHS_BALANCE")) AS unique_monthly_records
FROM raw.bureau_balance;

-- Verified Result:
-- Total Rows: 27,299,925
-- Unique Monthly Records: 27,299,925


-- ============================================================
-- Validation Summary
-- ============================================================
-- ✔ Total Rows               : 27,299,925
-- ✔ Total Columns            : 3
-- ✔ Unique Bureau Accounts   : 817,395
-- ✔ Monthly Records Verified : 27,299,925
--
-- Notes:
-- • Every (SK_ID_BUREAU, MONTHS_BALANCE) combination is unique.
-- • Each bureau account contains multiple monthly history records.
-- • The table has been successfully imported into PostgreSQL.
--
