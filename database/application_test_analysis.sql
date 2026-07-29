-- ============================================================
-- APPLICATION TEST BUSINESS ANALYSIS
-- Purpose: Analyze applicant demographics, financial profile,
-- and application characteristics.
-- ============================================================


-- ============================================================
-- 1. Contract Type Distribution
-- ============================================================

SELECT
    "NAME_CONTRACT_TYPE",
    COUNT(*) AS total_applications
FROM raw.application_test
GROUP BY "NAME_CONTRACT_TYPE"
ORDER BY total_applications DESC;

-- Result:
-- Cash loans      : 48,305
-- Revolving loans : 439


-- ============================================================
-- 2. Gender Distribution
-- ============================================================

SELECT
    "CODE_GENDER",
    COUNT(*) AS applicants
FROM raw.application_test
GROUP BY "CODE_GENDER"
ORDER BY applicants DESC;

-- Result:
-- Female : 32,678
-- Male   : 16,066


-- ============================================================
-- 3. Income Type Distribution
-- ============================================================

SELECT
    "NAME_INCOME_TYPE",
    COUNT(*) AS applicants
FROM raw.application_test
GROUP BY "NAME_INCOME_TYPE"
ORDER BY applicants DESC;

-- Result:
-- Working               : 24,533
-- Commercial Associate  : 11,402
-- Pensioner             : 9,273
-- State Servant         : 3,532
-- Student               : 2
-- Unemployed            : 1
-- Businessman           : 1


-- ============================================================
-- 4. Education Level
-- ============================================================

SELECT
    "NAME_EDUCATION_TYPE",
    COUNT(*) AS applicants
FROM raw.application_test
GROUP BY "NAME_EDUCATION_TYPE"
ORDER BY applicants DESC;

-- Result:
-- Secondary / Secondary Special : 33,988
-- Higher Education              : 12,516
-- Incomplete Higher             : 1,724
-- Lower Secondary               : 475
-- Academic Degree               : 41


-- ============================================================
-- 5. Housing Type
-- ============================================================

SELECT
    "NAME_HOUSING_TYPE",
    COUNT(*) AS applicants
FROM raw.application_test
GROUP BY "NAME_HOUSING_TYPE"
ORDER BY applicants DESC;

-- Result:
-- House / Apartment    : 43,645
-- With Parents         : 2,234
-- Municipal Apartment  : 1,617
-- Rented Apartment     : 718
-- Office Apartment     : 407
-- Co-op Apartment      : 123


-- ============================================================
-- 6. Average Income
-- ============================================================

SELECT
    ROUND(AVG("AMT_INCOME_TOTAL"),2) AS average_income
FROM raw.application_test;

-- Result:
-- Average Income: 178,431.81


-- ============================================================
-- 7. Average Credit Amount
-- ============================================================

SELECT
    ROUND(AVG("AMT_CREDIT"),2) AS average_credit
FROM raw.application_test;

-- Result:
-- Average Credit: 516,740.44


-- ============================================================
-- 8. Average Applicant Age
-- ============================================================

SELECT
    ROUND(AVG(ABS("DAYS_BIRTH")/365.25),2) AS average_age
FROM raw.application_test;

-- Result:
-- Average Age: 43.99 years


-- ============================================================
-- 9. Car Ownership
-- ============================================================

SELECT
    "FLAG_OWN_CAR",
    COUNT(*) AS applicants
FROM raw.application_test
GROUP BY "FLAG_OWN_CAR";

-- Result:
-- Yes : 16,433
-- No  : 32,311


-- ============================================================
-- 10. Property Ownership
-- ============================================================

SELECT
    "FLAG_OWN_REALTY",
    COUNT(*) AS applicants
FROM raw.application_test
GROUP BY "FLAG_OWN_REALTY";

-- Result:
-- Yes : 33,658
-- No  : 15,086


-- ============================================================
-- 11. Average Family Members
-- ============================================================

SELECT
    ROUND(AVG("CNT_FAM_MEMBERS"),2) AS average_family_members
FROM raw.application_test;

-- Result:
-- Average Family Members: 2.15


-- ============================================================
-- 12. Top Organization Types
-- ============================================================

SELECT
    "ORGANIZATION_TYPE",
    COUNT(*) AS applicants
FROM raw.application_test
GROUP BY "ORGANIZATION_TYPE"
ORDER BY applicants DESC
LIMIT 10;

-- Result:
-- Business Entity Type 3 : 10,840
-- XNA                    : 9,274
-- Self-employed          : 5,920
-- Other                  : 2,707
-- Medicine               : 1,716
-- Government             : 1,508
-- Business Entity Type 2 : 1,479
-- Trade: type 7          : 1,303
-- School                 : 1,287
-- Construction           : 1,039