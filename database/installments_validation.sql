-- ============================================================
-- INSTALLMENTS PAYMENTS TABLE VALIDATION
-- Purpose: Validate that installments_payments.csv has been
-- correctly loaded into the raw schema.
-- ============================================================


-- ============================================================
-- 1. Validate Total Row Count
-- ============================================================

SELECT COUNT(*) AS total_rows
FROM raw.installments_payments;

-- Verified Result:
-- Total Rows: 13,605,401


-- ============================================================
-- 2. Validate Total Column Count
-- ============================================================

SELECT COUNT(*) AS total_columns
FROM information_schema.columns
WHERE table_schema = 'raw'
AND table_name = 'installments_payments';

-- Verified Result:
-- Total Columns: 8


-- ============================================================
-- 3. Validate Unique Previous Loan IDs
-- ============================================================

SELECT COUNT(DISTINCT "SK_ID_PREV") AS unique_previous_loans
FROM raw.installments_payments;

-- Verified Result:
-- Unique Previous Loans: 997,752


-- ============================================================
-- 4. Validate Installment Record Uniqueness
-- Purpose:
-- Check uniqueness using the combination of loan ID,
-- installment number, and installment version.
-- ============================================================

SELECT
    COUNT(*) AS total_rows,
    COUNT(DISTINCT (
        "SK_ID_PREV",
        "NUM_INSTALMENT_NUMBER",
        "NUM_INSTALMENT_VERSION"
    )) AS unique_installment_records
FROM raw.installments_payments;

-- Verified Result:
-- Total Rows                 : 13,605,401
-- Unique Installment Records : 12,951,918


-- ============================================================
-- 5. Validate Unique Applicants
-- ============================================================

SELECT COUNT(DISTINCT "SK_ID_CURR") AS unique_applicants
FROM raw.installments_payments;

-- Verified Result:
-- Unique Applicants: 339,587


-- ============================================================
-- Validation Summary
-- ============================================================
-- ✔ Total Rows                  : 13,605,401
-- ✔ Total Columns               : 8
-- ✔ Unique Previous Loans       : 997,752
-- ✔ Unique Installment Records  : 12,951,918
-- ✔ Unique Applicants           : 339,587
--
-- Notes:
-- • SK_ID_PREV is expected to appear multiple times because
--   each previous loan consists of multiple installment payments.
--
-- • Some installment records share the same
--   (SK_ID_PREV, NUM_INSTALMENT_NUMBER, NUM_INSTALMENT_VERSION)
--   because a scheduled installment may be paid in multiple
--   transactions or adjusted over time.
--
