# FinShield – End-to-End Credit Risk Assessment & Decision Support System

## Project Overview

FinShield is an end-to-end credit risk assessment and decision-support system designed to predict the probability of loan default.

The project combines data engineering, SQL analytics, feature engineering, exploratory data analysis, machine learning, model evaluation, threshold optimization, and customer-level prediction into a single pipeline.

The system uses historical loan application and credit-history data to identify customers who may have a higher probability of default. The final machine learning model generates a default probability that is converted into a risk classification to support credit-risk decision making.

---

## Business Problem

Financial institutions need to assess the creditworthiness of customers before approving loans.

A major challenge is identifying customers who are likely to default while avoiding unnecessary rejection of customers who are likely to repay.

FinShield addresses this problem as a binary classification task:

- `0` → Non-Default
- `1` → Default

The primary objective is not simply to maximize accuracy. Since loan default is the minority class, the project focuses on metrics such as Recall, F1 Score, and ROC-AUC to evaluate the model's ability to identify potential defaulters.

---

## Project Objectives

The main objectives of FinShield are:

- Build an end-to-end credit-risk analytics pipeline.
- Load and validate multiple credit-related datasets.
- Perform SQL-based data analysis.
- Engineer customer-level features from historical financial records.
- Clean and prepare the master dataset for machine learning.
- Perform exploratory data analysis.
- Compare multiple machine learning algorithms.
- Handle class imbalance during model development.
- Evaluate different decision thresholds.
- Select a final machine learning model.
- Generate customer-level default-risk predictions.
- Provide a foundation for a credit-risk decision-support application.

---

# Dataset

FinShield uses the Home Credit dataset, which contains information about loan applications and customers' previous credit history.

The project works with multiple related datasets rather than relying only on the main loan application table.

## Main Datasets

| Dataset | Purpose |
|---|---|
| `application_train.csv` | Main training dataset containing loan applications and the target variable |
| `application_test.csv` | Application records used for prediction |
| `bureau.csv` | Customer credit history from other financial institutions |
| `bureau_balance.csv` | Monthly balance history of previous bureau credits |
| `previous_application.csv` | Customer's previous loan applications |
| `POS_CASH_balance.csv` | Monthly history of previous POS and cash loans |
| `installments_payments.csv` | Previous loan installment and payment history |
| `credit_card_balance.csv` | Monthly credit-card balance history |
| `HomeCredit_columns_description.csv` | Description of dataset columns |

## Target Variable

The primary target variable is:

```text
TARGET
```

Where:

- `0` → Customer did not default
- `1` → Customer defaulted

The target variable is highly imbalanced, with default cases representing a much smaller portion of the dataset. This class imbalance is an important consideration throughout the machine learning pipeline.

---

# Project Architecture

The overall FinShield pipeline is:

```text
Raw CSV Files
      ↓
Data Inspection & Validation
      ↓
PostgreSQL
      ↓
SQL Analysis
      ↓
Feature Engineering
      ↓
Customer-Level Feature Tables
      ↓
Feature Merging
      ↓
Data Cleaning
      ↓
Exploratory Data Analysis
      ↓
Train/Test Split
      ↓
Feature Encoding
      ↓
Model Training
      ↓
Model Comparison
      ↓
Threshold Optimization
      ↓
Final XGBoost Model
      ↓
Customer Risk Prediction
```

---

# Data Engineering

## Data Ingestion

The raw datasets are loaded into PostgreSQL and organized into separate database schemas.

Python ingestion scripts are used to load the datasets into the database.

The ingestion layer includes:

- Application training data
- Application test data
- Bureau data
- Bureau balance data
- Previous application data
- POS cash balance data
- Installment payment data
- Credit card balance data

The database layer provides structured storage for the datasets and allows SQL-based analysis and validation before feature engineering and machine learning.

---

## Database Structure

The project separates data into logical PostgreSQL schemas.

```text
PostgreSQL
│
├── raw
│   ├── application_train
│   ├── application_test
│   ├── bureau
│   ├── bureau_balance
│   ├── previous_application
│   ├── pos_cash_balance
│   ├── installments_payments
│   └── credit_card_balance
│
├── feature
│   ├── bureau_features
│   ├── bureau_balance_features
│   ├── previous_application_features
│   ├── pos_cash_balance_features
│   ├── installments_payments_features
│   └── credit_card_balance_features
│
└── analytics
```

This structure separates raw data from engineered features and analytical outputs.

---

# SQL Analysis

SQL was used to analyze and validate the datasets before feature engineering and machine learning.

Separate analysis and validation scripts were created for the major datasets.

## SQL Analysis Areas

The SQL analysis covers:

- Dataset structure
- Record counts
- Missing values
- Customer relationships
- Credit history
- Previous applications
- Installment payments
- Credit card behavior
- POS cash activity
- Bureau records
- Bureau balance history

Validation queries were also created to verify the database data and support reliable downstream processing.

## SQL Files

```text
database/
├── application_bureau_analysis.sql
├── application_test_analysis.sql
├── application_test_validation.sql
├── application_validation.sql
├── bureau_balance_analysis.sql
├── bureau_balance_validation.sql
├── bureau_validation.sql
├── credit_card_analysis.sql
├── credit_card_validation.sql
├── installments_analysis.sql
├── installments_validation.sql
├── pos_cash_analysis.sql
├── pos_cash_validation.sql
├── previous_application_analysis.sql
└── previous_application_validation.sql
```

---

# Feature Engineering

The historical credit datasets contain multiple records for the same customer.

Instead of directly using these transactional records, FinShield transforms them into customer-level aggregated features.

The general process is:

```text
Historical Transaction Data
          ↓
Group by Customer
          ↓
Numerical Aggregations
          ↓
Categorical Aggregations
          ↓
Derived Ratios
          ↓
Customer-Level Feature Table
```

## Bureau Features

The `bureau` dataset contains information about customers' previous credits from other financial institutions.

Features were aggregated at the customer level using numerical and categorical information.

The resulting bureau feature table contains:

```text
63 customer-level features
```

Output:

```text
data/final/bureau_features.csv
```

---

## Bureau Balance Features

The `bureau_balance` dataset contains monthly balance information for previous bureau credits.

The feature engineering process included:

- Monthly balance statistics
- Minimum and maximum months
- Record counts
- Credit-status counts
- Mapping bureau accounts back to customers
- Customer-level aggregation

Categorical credit-status values were converted into numerical count features.

The resulting dataset contains:

```text
134,542 rows
34 columns
```

Memory optimization reduced the dataframe memory usage from approximately:

```text
34.90 MB → 10.01 MB
```

This represents approximately a 71% reduction in memory usage.

Output:

```text
data/final/bureau_balance_features.csv
```

---

## Previous Application Features

The `previous_application` dataset contains customers' historical loan applications.

Features were generated using:

- Numerical aggregations
- Contract-status counts
- Contract-type counts
- Customer-level aggregation
- Ratio-based features

Two derived ratios include:

```text
prev_credit_application_ratio
=
prev_amt_credit_mean / prev_amt_application_mean
```

and:

```text
prev_annuity_credit_ratio
=
prev_amt_annuity_mean / prev_amt_credit_mean
```

The resulting feature table contains:

```text
338,857 rows
26 columns
```

Output:

```text
data/final/previous_application_features.csv
```

---

## Other Historical Features

Customer-level features were also generated from:

- `POS_CASH_balance`
- `installments_payments`
- `credit_card_balance`

These datasets provide additional information about:

- Previous loan repayment behavior
- Installment payment patterns
- POS/cash loan activity
- Credit card utilization and balances

The resulting feature tables are stored under:

```text
data/final/
```

---

# Feature Merging

After generating customer-level features from the individual historical datasets, the feature tables are merged with the main application dataset using the customer identifier.

The resulting master dataset combines:

```text
Application Information
        +
Bureau Features
        +
Bureau Balance Features
        +
Previous Application Features
        +
POS Cash Features
        +
Installment Features
        +
Credit Card Features
```

The merged dataset is stored as:

```text
data/final/master_dataset.csv
```

---

# Data Cleaning & Preprocessing

The merged master dataset contains a large number of numerical and categorical variables.

The preprocessing stage prepares the data for machine learning.

The process includes:

- Handling missing values
- Separating the target variable
- Preparing numerical features
- Preparing categorical features
- Removing unsuitable columns
- Encoding categorical variables
- Aligning training and test features
- Preparing the final machine-learning dataset

The cleaned dataset is stored as:

```text
data/final/clean_master_dataset.csv
```

---

# Exploratory Data Analysis

Exploratory Data Analysis was performed to understand the distribution of important variables and relationships within the dataset.

## Analysis Performed

The analysis includes:

- Dataset overview
- Target distribution
- Numerical feature distributions
- Outlier analysis
- Correlation analysis
- Feature selection analysis

## Visualizations

Visualizations were generated for important variables including:

- `AMT_INCOME_TOTAL`
- `AMT_CREDIT`
- `AMT_ANNUITY`
- `AMT_GOODS_PRICE`
- `DAYS_BIRTH`
- `DAYS_EMPLOYED`

Additional visualizations include:

- Target distribution
- Correlation heatmap
- Histograms
- Boxplots

All generated figures are stored under:

```text
reports/figures/
```

---

# Machine Learning

FinShield treats credit default prediction as a binary classification problem.

The target classes are:

```text
0 → Non-Default
1 → Default
```

Because the default class is significantly smaller than the non-default class, accuracy alone is not sufficient for evaluating model performance.

The project therefore considers:

- Accuracy
- Precision
- Recall
- F1 Score
- ROC-AUC

---

# Feature Encoding

The dataset contains categorical variables that cannot be directly processed by the machine-learning models.

Categorical variables were converted using one-hot encoding.

The final encoded feature matrix contained:

```text
432 features
```

The encoded training and testing datasets had the following shapes:

```text
Training: 246,008 × 432
Testing:   61,503 × 432
```

One-hot encoding was used to represent categorical variables numerically without imposing an artificial ordinal relationship between categories.

---

# Model Development

Multiple machine learning algorithms were trained and evaluated.

The models include:

1. Logistic Regression
2. Random Forest
3. XGBoost
4. LightGBM

This allowed the project to compare linear and tree-based approaches for credit-risk classification.

---

# Model Comparison

The evaluated models produced the following results:

| Model | Accuracy | Precision | Recall | F1 Score | ROC-AUC |
|---|---:|---:|---:|---:|---:|
| Logistic Regression | 0.9190 | 0.4679 | 0.0264 | 0.0500 | 0.7733 |
| Random Forest | 0.7598 | 0.1851 | 0.5805 | 0.2807 | 0.7507 |
| XGBoost | **0.8540** | 0.2645 | **0.4538** | **0.3342** | **0.7845** |
| LightGBM | 0.8545 | 0.2636 | 0.4475 | 0.3318 | 0.7831 |

## Model Selection

XGBoost was selected as the final model.

Although Logistic Regression achieved higher accuracy, it had very low recall for the minority default class.

XGBoost achieved:

- Highest F1 Score: `0.3342`
- Highest ROC-AUC: `0.7845`
- Strong recall for the minority default class

Therefore, XGBoost provided the best overall balance among the evaluated models for identifying potential default cases.

---

# Final XGBoost Model

The final model is:

```text
XGBoost Classifier
```

The trained model is stored as:

```text
models/xgboost_model.pkl
```

The corresponding training feature names are stored as:

```text
models/xgboost_features.pkl
```

The trained datasets and target variables are also stored in the `models/` directory.

---

# Threshold Optimization

Classification models generate probabilities that must be converted into class predictions using a decision threshold.

Instead of relying only on the default threshold of `0.50`, FinShield evaluates multiple thresholds.

## Threshold Comparison

| Threshold | Precision | Recall | F1 Score |
|---:|---:|---:|---:|
| 0.30 | 0.3810 | 0.1641 | 0.2294 |
| 0.25 | 0.3519 | 0.2302 | 0.2783 |
| 0.20 | 0.3121 | 0.3257 | 0.3187 |
| **0.15** | **0.2645** | **0.4538** | **0.3342** |

The threshold of:

```text
0.15
```

was selected because it achieved the highest F1 Score among the evaluated thresholds while substantially improving recall for the minority default class.

---

# Business Interpretation

The threshold selection reflects the nature of credit-risk assessment.

A false negative occurs when a customer who is likely to default is classified as non-default.

A false positive occurs when a potentially safe customer is classified as high risk.

In a credit-risk context, missing a potential defaulter can be costly. Therefore, the system gives greater consideration to identifying potential default cases rather than maximizing overall accuracy alone.

The selected threshold of `0.15` allows the system to flag customers at a lower probability threshold, increasing the model's ability to identify potential high-risk customers.

The appropriate threshold should ultimately depend on the financial institution's risk appetite and the actual business cost of false positives versus false negatives.

---

# Final Model Evaluation

The final XGBoost model produced the following evaluation results:

```text
Accuracy  : 0.8540
Precision : 0.2645
Recall    : 0.4538
F1 Score  : 0.3342
ROC-AUC   : 0.7845
```

## Confusion Matrix

```text
[[50273, 6265],
 [ 2712, 2253]]
```

The confusion matrix provides a detailed view of correct and incorrect predictions across the non-default and default classes.

---

# Model Explainability

Model explainability is an important consideration for credit-risk applications because predictions should be understandable rather than treated as a black box.

SHAP was used as part of the model interpretation workflow to analyze feature contributions to model predictions.

The purpose of the explainability analysis is to understand which features contribute to predictions and provide greater transparency around the model's decision-making process.

---

# Customer Risk Prediction

FinShield includes a prediction pipeline that takes customer-level input data and generates a risk assessment.

The prediction workflow is:

```text
Customer Input
      ↓
Feature Alignment
      ↓
One-Hot Encoding
      ↓
XGBoost Prediction
      ↓
Default Probability
      ↓
Risk Classification
```

The prediction script can be executed using:

```bash
python -m src.modeling.predict
```

The system loads the trained XGBoost model and aligns incoming customer features with the features used during training.

The final classification threshold is:

```text
0.15
```

The output includes:

- Customer identifier
- Default probability
- Risk level
- Default/non-default prediction

## Example Prediction

```text
FinShield : Customer 1
Default Probability : 1.83%
Risk Level : LOW RISK
Prediction : NON-DEFAULT
```

---

# Project Structure

```text
FinShield/
│
├── app/
│   └── dashboard/
│
├── data/
│   ├── prediction_input.csv
│   │
│   ├── final/
│   │   ├── bureau_balance_features.csv
│   │   ├── bureau_features.csv
│   │   ├── clean_master_dataset.csv
│   │   ├── credit_card_balance_features.csv
│   │   ├── installments_payments_features.csv
│   │   ├── master_dataset.csv
│   │   ├── pos_cash_balance_features.csv
│   │   └── previous_application_features.csv
│   │
│   ├── processed/
│   │   └── bureau_features.csv
│   │
│   └── raw/
│       ├── application_test.csv
│       ├── application_train.csv
│       ├── bureau.csv
│       ├── bureau_balance.csv
│       ├── credit_card_balance.csv
│       ├── HomeCredit_columns_description.csv
│       ├── installments_payments.csv
│       ├── POS_CASH_balance.csv
│       ├── previous_application.csv
│       └── sample_submission.csv
│
├── database/
│   ├── application_bureau_analysis.sql
│   ├── application_test_analysis.sql
│   ├── application_test_validation.sql
│   ├── application_validation.sql
│   ├── bureau_balance_analysis.sql
│   ├── bureau_balance_validation.sql
│   ├── bureau_validation.sql
│   ├── credit_card_analysis.sql
│   ├── credit_card_validation.sql
│   ├── installments_analysis.sql
│   ├── installments_validation.sql
│   ├── pos_cash_analysis.sql
│   ├── pos_cash_validation.sql
│   ├── previous_application_analysis.sql
│   └── previous_application_validation.sql
│
├── models/
│   ├── lightgbm_model.pkl
│   ├── logistic_regression_model.pkl
│   ├── logistic_regression_scaler.pkl
│   ├── random_forest_model.pkl
│   ├── xgboost_features.pkl
│   ├── xgboost_model.pkl
│   ├── X_test.pkl
│   ├── X_train.pkl
│   ├── y_test.pkl
│   └── y_train.pkl
│
├── notebooks/
│
├── reports/
│   └── figures/
│
├── results/
│   ├── final_model_metrics.txt
│   ├── model_comparison.csv
│   └── threshold_comparison.csv
│
├── src/
│   ├── analysis/
│   │   ├── correlation_analysis.py
│   │   ├── dataset_overview.py
│   │   ├── feature_selection.py
│   │   ├── numerical_analysis.py
│   │   └── target_analysis.py
│   │
│   ├── deployment/
│   │
│   ├── feature_configs/
│   │
│   ├── feature_engineering/
│   │
│   ├── ingestion/
│   │
│   ├── inspection/
│   │
│   ├── modeling/
│   │
│   └── preprocessing/
│
└── README.md
```

---

# Technologies Used

## Programming & Data Analysis

- Python
- Pandas
- NumPy

## Database

- PostgreSQL
- SQLAlchemy
- SQL

## Machine Learning

- Scikit-learn
- XGBoost
- LightGBM

## Data Visualization

- Matplotlib
- Seaborn

## Model Explainability

- SHAP

## Development Tools

- Git
- GitHub
- Python Virtual Environment

---

# Key Skills Demonstrated

This project demonstrates practical experience in:

- Python programming
- SQL
- PostgreSQL
- Data ingestion
- Data validation
- Data cleaning
- Exploratory Data Analysis
- Feature engineering
- Customer-level aggregation
- Categorical encoding
- Class-imbalance handling
- Machine learning
- Model comparison
- Classification evaluation
- Threshold optimization
- Model persistence
- Prediction pipelines
- Model explainability
- Credit-risk analytics
- End-to-end project development

---

# Results & Key Takeaways

FinShield demonstrates how multiple sources of customer financial history can be transformed into a machine-learning-ready dataset for credit-risk prediction.

Key findings from the modeling process include:

- Accuracy alone was not sufficient for evaluating the models because of class imbalance.
- Logistic Regression achieved high accuracy but very low recall for the default class.
- Tree-based models provided stronger minority-class detection.
- XGBoost achieved the highest F1 Score and ROC-AUC among the evaluated models.
- Lowering the classification threshold improved recall for potential default cases.
- A threshold of `0.15` achieved the highest F1 Score among the evaluated thresholds.
- Customer-level probability and risk classification make the model output easier to interpret from a decision-support perspective.

---

# Future Improvements

Potential future improvements include:

- Hyperparameter optimization using systematic search techniques.
- Cost-sensitive model evaluation using an explicit business cost matrix.
- Calibration of predicted default probabilities.
- Additional feature selection techniques.
- More extensive SHAP-based model explainability.
- Deployment of the prediction pipeline through a user-facing application.
- Integration with a business intelligence dashboard.
- Model monitoring and performance tracking after deployment.

---

# Installation & Usage

## 1. Clone the Repository

```bash
git clone <repository-url>
cd FinShield
```

## 2. Create a Virtual Environment

```bash
python -m venv venv
```

## 3. Activate the Environment

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

## 4. Install Dependencies

Install the required Python packages using the project's dependency file.

```bash
pip install -r requirements.txt
```

## 5. Configure PostgreSQL

Configure the PostgreSQL connection details in:

```text
src/config.py
```

## 6. Run the Prediction Pipeline

```bash
python -m src.modeling.predict
```

The prediction pipeline loads the trained XGBoost model, prepares the input features, generates the default probability, and produces the corresponding risk classification.

---

# Conclusion

FinShield provides an end-to-end approach to credit-risk assessment, starting from raw financial datasets and ending with customer-level default-risk predictions.

The project combines:

```text
Data Engineering
        +
SQL Analytics
        +
Feature Engineering
        +
EDA
        +
Machine Learning
        +
Model Evaluation
        +
Threshold Optimization
        +
Model Explainability
        +
Risk Prediction
```

By combining these components, FinShield demonstrates a practical machine-learning workflow for solving an imbalanced credit-risk classification problem and translating model predictions into a decision-support format.

---

# Author

**Afrin Taj**

Aspiring Data Scientist | Machine Learning | Data Analytics
