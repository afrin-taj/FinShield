-- ============================================================
-- POS_CASH_BALANCE TABLE VALIDATION
-- Purpose: Validate that POS_CASH_balance.csv has been
-- successfully loaded into PostgreSQL.
-- ============================================================


-- ============================================================
-- 1. Total Rows
-- ============================================================

SELECT COUNT(*) AS total_rows
FROM raw.pos_cash_balance;

-- Verified Result:
-- Total Rows: 7,750,000


-- ============================================================
-- 2. Total Columns
-- ============================================================

SELECT COUNT(*) AS total_columns
FROM information_schema.columns
WHERE table_schema = 'raw'
AND table_name = 'pos_cash_balance';

-- Verified Result:
-- Total Columns: 8


-- ============================================================
-- 3. Unique Previous Loans
-- ============================================================

SELECT COUNT(DISTINCT "SK_ID_PREV") AS unique_previous_loans
FROM raw.pos_cash_balance;

-- Verified Result:
-- Unique Previous Loans: 926,571


-- ============================================================
-- 4. Unique Applicants
-- ============================================================

SELECT COUNT(DISTINCT "SK_ID_CURR") AS unique_applicants
FROM raw.pos_cash_balance;

-- Verified Result:
-- Unique Applicants: 336,704


-- ============================================================
-- 5. Monthly Record Validation
-- ============================================================

SELECT
    COUNT(*) AS total_rows,
    COUNT(DISTINCT ("SK_ID_PREV", "MONTHS_BALANCE")) AS unique_monthly_records
FROM raw.pos_cash_balance;

-- Verified Result:
-- Total Rows: 7,750,000
-- Unique Monthly Records: 7,750,000


-- ============================================================
-- Validation Summary
-- ============================================================
-- ✔ Total Rows               : 7,750,000
-- ✔ Total Columns            : 8
-- ✔ Unique Previous Loans    : 926,571
-- ✔ Unique Applicants        : 336,704
-- ✔ Unique Monthly Records   : 7,750,000
--
-- Notes:
-- • Each (SK_ID_PREV, MONTHS_BALANCE) combination is unique,
--   confirming that every monthly snapshot is stored only once.
--
-- • SK_ID_PREV repeats because one loan has multiple monthly records.
--
-- • SK_ID_CURR repeats because one customer can have multiple loans.
--
