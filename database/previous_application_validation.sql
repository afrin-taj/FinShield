-- ============================================================
-- PREVIOUS APPLICATION TABLE VALIDATION
-- Purpose: Validate that previous_application.csv has been
-- correctly loaded into the raw schema.
-- ============================================================


-- ============================================================
-- 1. Validate Total Row Count
-- ============================================================

SELECT COUNT(*) AS total_rows
FROM raw.previous_application;

-- Verified Result:
-- Total Rows: 1,670,214


-- ============================================================
-- 2. Validate Total Column Count
-- ============================================================

SELECT COUNT(*) AS total_columns
FROM information_schema.columns
WHERE table_schema = 'raw'
AND table_name = 'previous_application';

-- Verified Result:
-- Total Columns: 37


-- ============================================================
-- 3. Validate Unique Previous Application IDs
-- ============================================================

SELECT COUNT(DISTINCT "SK_ID_PREV") AS unique_previous_applications
FROM raw.previous_application;

-- Verified Result:
-- Unique Previous Applications: 1,670,214


-- ============================================================
-- 4. Check Duplicate Previous Application IDs
-- ============================================================

SELECT
    "SK_ID_PREV",
    COUNT(*) AS occurrence_count
FROM raw.previous_application
GROUP BY "SK_ID_PREV"
HAVING COUNT(*) > 1;

-- Verified Result:
-- No duplicate SK_ID_PREV found (0 rows returned)


-- ============================================================
-- 5. Count Unique Applicants
-- ============================================================

SELECT COUNT(DISTINCT "SK_ID_CURR") AS unique_applicants
FROM raw.previous_application;

-- Verified Result:
-- Unique Applicants: 338,857


-- ============================================================
-- Validation Summary
-- ============================================================
-- ✔ Total Rows                  : 1,670,214
-- ✔ Total Columns               : 37
-- ✔ Unique SK_ID_PREV           : 1,670,214
-- ✔ Duplicate SK_ID_PREV        : 0
-- ✔ Unique Applicants           : 338,857

