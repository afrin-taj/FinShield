-- ============================================================
-- 1. Validate total row count
-- Purpose: Confirm that all rows from application_train.csv
-- were successfully loaded into PostgreSQL.
-- ============================================================

SELECT COUNT(*) AS total_rows
FROM raw.application_train;

-- Verified result: 307,511 rows


-- ============================================================
-- 2. Validate total column count
-- Purpose: Confirm that no columns were lost during ingestion.
-- ============================================================

SELECT COUNT(*) AS total_columns
FROM information_schema.columns
WHERE table_schema = 'raw'
  AND table_name = 'application_train';

-- Verified result: 122 columns


-- ============================================================
-- 3. Validate unique applicant IDs
-- Purpose: Confirm that each applicant has a unique SK_ID_CURR.
-- ============================================================

SELECT
    COUNT(*) AS total_rows,
    COUNT(DISTINCT "SK_ID_CURR") AS unique_applicants
FROM raw.application_train;

-- Verified result:
-- Total rows: 307,511
-- Unique applicants: 307,511


-- ============================================================
-- 4. Check for duplicate applicant IDs
-- Purpose: Ensure no duplicate records were created during ingestion.
-- ============================================================

SELECT
    "SK_ID_CURR",
    COUNT(*) AS occurrence_count
FROM raw.application_train
GROUP BY "SK_ID_CURR"
HAVING COUNT(*) > 1;

-- Verified result: 0 duplicate applicant IDs


-- ============================================================
-- 5. Validate target distribution
-- Purpose: Confirm that the target distribution matches the source CSV.
-- ============================================================

SELECT
    "TARGET",
    COUNT(*) AS applicant_count,
    ROUND(
        COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (),
        2
    ) AS percentage
FROM raw.application_train
GROUP BY "TARGET"
ORDER BY "TARGET";

-- Verified result:
-- TARGET 0: 282,686 applicants (91.93%)
-- TARGET 1:  24,825 applicants (8.07%)