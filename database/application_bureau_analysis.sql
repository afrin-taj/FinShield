-- ============================================================
-- APPLICATION & BUREAU RELATIONSHIP ANALYSIS
-- Purpose: Explore the relationship between loan applicants
-- and their historical credit records.
-- ============================================================


-- ============================================================
-- 1. Applicants with Bureau History
-- Purpose: Count applicants having at least one bureau record.
-- ============================================================

SELECT COUNT(DISTINCT b."SK_ID_CURR") AS applicants_with_bureau_history
FROM raw.bureau b;

-- Verified Result:
-- Applicants with Bureau History: 305,811


-- ============================================================
-- 2. Applicants without Bureau History
-- Purpose: Identify applicants with no previous credit records.
-- ============================================================

SELECT COUNT(*) AS applicants_without_bureau_history
FROM raw.application_train a
LEFT JOIN raw.bureau b
ON a."SK_ID_CURR" = b."SK_ID_CURR"
WHERE b."SK_ID_CURR" IS NULL;

-- Verified Result:
-- Applicants without Bureau History: 44,020


-- ============================================================
-- 3. Top 10 Applicants by Previous Credit Records
-- Purpose: Find applicants having the highest number of
-- historical credit records.
-- ============================================================

SELECT
    a."SK_ID_CURR",
    COUNT(b."SK_ID_BUREAU") AS total_previous_credits
FROM raw.application_train a
LEFT JOIN raw.bureau b
ON a."SK_ID_CURR" = b."SK_ID_CURR"
GROUP BY a."SK_ID_CURR"
ORDER BY total_previous_credits DESC
LIMIT 10;

-- Verified Result:
-- SK_ID_CURR | Total Previous Credits
-- 120860     | 116
-- 169704     | 94
-- 251643     | 61
-- 295809     | 59
-- 129843     | 58
-- 177014     | 56
-- 218175     | 55
-- 280155     | 55
-- 430261     | 54
-- 281455     | 54


-- ============================================================
-- 4. Average Previous Credit Records per Applicant
-- Purpose: Calculate the average number of bureau records
-- associated with each applicant.
-- ============================================================

SELECT
    ROUND(AVG(credit_count),2) AS avg_previous_credits
FROM
(
    SELECT
        a."SK_ID_CURR",
        COUNT(b."SK_ID_BUREAU") AS credit_count
    FROM raw.application_train a
    LEFT JOIN raw.bureau b
    ON a."SK_ID_CURR" = b."SK_ID_CURR"
    GROUP BY a."SK_ID_CURR"
) t;

-- Verified Result:
-- Average Previous Credits: 4.77


-- ============================================================
-- 5. Credit Status Distribution
-- Purpose: Analyze the status of previous credit accounts.
-- ============================================================

SELECT
    "CREDIT_ACTIVE",
    COUNT(*) AS total_records
FROM raw.bureau
GROUP BY "CREDIT_ACTIVE"
ORDER BY total_records DESC;

-- Verified Result:
-- Closed   : 1,079,273
-- Active   :   630,607
-- Sold     :     6,527
-- Bad debt :        21


-- ============================================================
-- Business Insights
-- ============================================================
-- • 305,811 applicants have at least one historical credit record.
-- • 44,020 applicants have no bureau history.
-- • Applicants have an average of 4.77 previous credit records.
-- • Most historical loans are Closed, indicating many applicants
--   have completed previous borrowing cycles.
-- • A significant number of Active loans suggests many applicants
--   are managing ongoing credit obligations.
-- • Very few accounts are classified as Bad Debt, making them
--   potentially valuable indicators for credit risk analysis.