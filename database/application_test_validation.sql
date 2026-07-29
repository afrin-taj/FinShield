-- ============================================================
-- APPLICATION TEST TABLE VALIDATION
-- Purpose: Validate that application_test.csv has been
-- successfully loaded into PostgreSQL.
-- ============================================================

-- ============================================================
-- 1. Total Rows
-- ============================================================

SELECT COUNT(*) AS total_rows
FROM raw.application_test;

-- Verified Result:
-- Total Rows: 48,744


-- ============================================================
-- 2. Total Columns
-- ============================================================

SELECT COUNT(*) AS total_columns
FROM information_schema.columns
WHERE table_schema = 'raw'
AND table_name = 'application_test';

-- Verified Result:
-- Total Columns: 121


-- ============================================================
-- 3. Unique Applicants
-- ============================================================

SELECT COUNT(DISTINCT "SK_ID_CURR") AS unique_applicants
FROM raw.application_test;

-- Verified Result:
-- Unique Applicants: 48,744


-- ============================================================
-- Validation Summary
-- ============================================================
-- ✔ Total Rows         : 48,744
-- ✔ Total Columns      : 121
-- ✔ Unique Applicants  : 48,744
--
-- Notes:
-- • Every applicant has a unique SK_ID_CURR.
-- • The dataset contains no TARGET column, as it is intended
--   for prediction on unseen applicants.

