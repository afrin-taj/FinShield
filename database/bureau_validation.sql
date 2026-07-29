-- ============================================================
-- BUREAU TABLE VALIDATION
-- Purpose: Validate that bureau.csv has been correctly loaded
-- into the raw schema of the FinShield database.
-- ============================================================


-- ============================================================
-- 1. Validate Total Row Count
-- Purpose: Ensure all records from bureau.csv were imported.
-- ============================================================

SELECT COUNT(*) AS total_rows
FROM raw.bureau;

-- Verified Result:
-- Total Rows: 1,716,428


-- ============================================================
-- 2. Validate Total Column Count
-- Purpose: Ensure all columns were imported successfully.
-- ============================================================

SELECT COUNT(*) AS total_columns
FROM information_schema.columns
WHERE table_schema = 'raw'
  AND table_name = 'bureau';

-- Verified Result:
-- Total Columns: 17


-- ============================================================
-- 3. Validate Unique Bureau IDs
-- Purpose: Each bureau record should have a unique identifier.
-- ============================================================

SELECT COUNT(DISTINCT "SK_ID_BUREAU") AS unique_bureau_ids
FROM raw.bureau;

-- Verified Result:
-- Unique SK_ID_BUREAU: 1,716,428


-- ============================================================
-- 4. Check for Duplicate Bureau IDs
-- Purpose: Ensure no duplicate bureau records exist.
-- ============================================================

SELECT
    "SK_ID_BUREAU",
    COUNT(*) AS occurrence_count
FROM raw.bureau
GROUP BY "SK_ID_BUREAU"
HAVING COUNT(*) > 1;

-- Verified Result:
-- No duplicate SK_ID_BUREAU found (0 rows returned)


-- ============================================================
-- 5. Validate Unique Applicants
-- Purpose: Count distinct applicants with bureau history.
-- ============================================================

SELECT COUNT(DISTINCT "SK_ID_CURR") AS unique_applicants
FROM raw.bureau;

-- Verified Result:
-- Unique Applicants: 305,811


-- ============================================================
-- Validation Summary
-- ============================================================
-- ✔ Total Rows             : 1,716,428
-- ✔ Total Columns          : 17
-- ✔ Unique SK_ID_BUREAU    : 1,716,428
-- ✔ Duplicate Bureau IDs   : 0
-- ✔ Unique Applicants      : 305,811
--
