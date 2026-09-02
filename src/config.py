"""
Project Configuration File
--------------------------
Stores all project-wide constants and settings.
"""

from pathlib import Path

# ==========================
# Project Root Directory
# ==========================
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# ==========================
# Data Directories
# ==========================
DATA_DIR = PROJECT_ROOT / "Data"

RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
FINAL_DATA_DIR = DATA_DIR / "final"

MODELS_DIR = PROJECT_ROOT / "models"
MODELS_DIR.mkdir(exist_ok=True)

# ==========================
# Database Schemas
# ==========================
RAW_SCHEMA = "raw"
FEATURE_SCHEMA = "feature"
ANALYTICS_SCHEMA = "analytics"

# ==========================
# Output Table Names
# ==========================
BUREAU_FEATURE_TABLE = "bureau_features"
BUREAU_BALANCE_FEATURE_TABLE = "bureau_balance_features"
PREVIOUS_APPLICATION_FEATURE_TABLE = "previous_application_features"
INSTALLMENTS_FEATURE_TABLE = "installments_features"
POS_CASH_FEATURE_TABLE = "pos_cash_features"
CREDIT_CARD_FEATURE_TABLE = "credit_card_features"

# ==========================
# Random Seed
# ==========================
RANDOM_STATE = 42