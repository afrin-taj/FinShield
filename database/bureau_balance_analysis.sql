-- ============================================================
-- BUREAU BALANCE BUSINESS ANALYSIS
-- Purpose: Analyze monthly bureau credit history and
-- repayment behavior.
-- ============================================================


-- ============================================================
-- 1. Credit Status Distribution
-- ============================================================

SELECT
    "STATUS",
    COUNT(*) AS total_records
FROM raw.bureau_balance
GROUP BY "STATUS"
ORDER BY total_records DESC;

-- Result:
-- C : 13,646,993
-- 0 : 7,499,507
-- X : 5,810,482
-- 1 :   242,347
-- 5 :    62,406
-- 2 :    23,419
-- 3 :     8,924
-- 4 :     5,847


-- ============================================================
-- 2. Closed Accounts
-- ============================================================

SELECT COUNT(*) AS closed_accounts
FROM raw.bureau_balance
WHERE "STATUS"='C';

-- Result:
-- 13,646,993


-- ============================================================
-- 3. Active Accounts
-- ============================================================

SELECT COUNT(*) AS active_accounts
FROM raw.bureau_balance
WHERE "STATUS"='0';

-- Result:
-- 7,499,507


-- ============================================================
-- 4. Overdue 30+ Days
-- ============================================================

SELECT COUNT(*) AS overdue_30_days
FROM raw.bureau_balance
WHERE "STATUS"='1';

-- Result:
-- 242,347


-- ============================================================
-- 5. Overdue 60+ Days
-- ============================================================

SELECT COUNT(*) AS overdue_60_days
FROM raw.bureau_balance
WHERE "STATUS"='2';

-- Result:
-- 23,419


-- ============================================================
-- 6. Overdue 90+ Days
-- ============================================================

SELECT COUNT(*) AS overdue_90_days
FROM raw.bureau_balance
WHERE "STATUS"='3';

-- Result:
-- 8,924


-- ============================================================
-- 7. Overdue 120+ Days
-- ============================================================

SELECT COUNT(*) AS overdue_120_days
FROM raw.bureau_balance
WHERE "STATUS"='4';

-- Result:
-- 5,847


-- ============================================================
-- 8. Overdue 150+ Days
-- ============================================================

SELECT COUNT(*) AS overdue_150_days
FROM raw.bureau_balance
WHERE "STATUS"='5';

-- Result:
-- 62,406


-- ============================================================
-- 9. Unknown Status
-- ============================================================

SELECT COUNT(*) AS unknown_status
FROM raw.bureau_balance
WHERE "STATUS"='X';

-- Result:
-- 5,810,482


-- ============================================================
-- 10. Bureau History Range
-- ============================================================

SELECT
    MIN("MONTHS_BALANCE") AS earliest_month,
    MAX("MONTHS_BALANCE") AS latest_month
FROM raw.bureau_balance;

-- Result:
-- Earliest : -96
-- Latest   : 0


-- ============================================================
-- 11. Longest Bureau History
-- ============================================================

SELECT
    "SK_ID_BUREAU",
    COUNT(*) AS history_months
FROM raw.bureau_balance
GROUP BY "SK_ID_BUREAU"
ORDER BY history_months DESC
LIMIT 10;

-- Result:
-- Longest history = 97 months


-- ============================================================
-- 12. Credit Status Percentage
-- ============================================================

SELECT
    "STATUS",
    COUNT(*) AS total_records,
    ROUND(
        COUNT(*)*100.0/
        SUM(COUNT(*)) OVER(),
        2
    ) AS percentage
FROM raw.bureau_balance
GROUP BY "STATUS"
ORDER BY total_records DESC;

-- Result:
-- C : 49.99%
-- 0 : 27.47%
-- X : 21.28%
-- 1 : 0.89%
-- 5 : 0.23%
-- 2 : 0.09%
-- 3 : 0.03%
-- 4 : 0.02%