import streamlit as st
import pandas as pd
import joblib

from src.config import MODELS_DIR
from src.modeling.predict import prepare_features, predict
from src.modeling.explain_prediction import explain_customer


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="FinShield",
    page_icon="🛡️",
    layout="centered"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* ==============================
       MAIN CONTENT
       ============================== */

    .block-container {
        max-width: 1100px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }


    /* ==============================
       MAIN TITLE
       ============================== */

    .main-title {
        font-size: 42px;
        font-weight: 700;
        color: #0F5132;
        margin-bottom: 0;
    }

    .subtitle {
        font-size: 17px;
        color: #198754;
        font-weight: 500;
        margin-top: 5px;
        margin-bottom: 10px;
    }

    .description {
        color: #5F6F64;
        margin-bottom: 30px;
    }


    /* ==============================
       SECTION HEADINGS
       ============================== */

    .section-title {
        font-size: 24px;
        font-weight: 600;
        color: #0F5132;
        margin-top: 25px;
        margin-bottom: 15px;
    }


    /* ==============================
       INFORMATION CARDS
       ============================== */

    .info-card {
        padding: 15px 18px;
        border: 1px solid #B7DCC8;
        border-radius: 10px;
        background-color: #F3FAF6;
        min-height: 85px;
        box-shadow: 0 2px 6px rgba(15, 81, 50, 0.08);
    }

    .card-label {
        font-size: 13px;
        color: #6C7A72;
        margin-bottom: 5px;
    }

    .card-value {
        font-size: 18px;
        font-weight: 600;
        color: #0F5132;
    }


    /* ==============================
       RISK RESULT CARD
       ============================== */

    .risk-card {
        padding: 25px;
        border: 1px solid #B7DCC8;
        border-radius: 12px;
        background-color: #F3FAF6;
        text-align: center;
        margin-top: 15px;
        box-shadow: 0 3px 10px rgba(15, 81, 50, 0.10);
    }

    .risk-probability {
        font-size: 42px;
        font-weight: 700;
        color: #198754;
    }

    .risk-label {
        font-size: 14px;
        color: #6C7A72;
    }


    /* ==============================
       STREAMLIT BUTTON
       ============================== */

    .stButton > button {
        background-color: #198754;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 1.5rem;
        font-weight: 600;
        transition: 0.2s;
    }

    .stButton > button:hover {
        background-color: #146C43;
        color: white;
        border: none;
    }


    /* ==============================
       SELECT BOX
       ============================== */

    div[data-baseweb="select"] > div {
        border-color: #B7DCC8;
    }

    div[data-baseweb="select"] > div:focus-within {
        border-color: #198754;
        box-shadow: 0 0 0 1px #198754;
    }


    /* ==============================
       INPUT BOX
       ============================== */

    input {
        border-color: #B7DCC8 !important;
    }

    input:focus {
        border-color: #198754 !important;
        box-shadow: 0 0 0 1px #198754 !important;
    }


    /* ==============================
       EXPANDERS
       ============================== */

    div[data-testid="stExpander"] {
        border: 1px solid #B7DCC8;
        border-radius: 10px;
    }


    /* ==============================
       SUCCESS MESSAGE
       ============================== */

    div[data-testid="stAlert"] {
        border-radius: 10px;
    }


    /* ==============================
       PROGRESS BAR
       ============================== */

    div[data-testid="stProgress"] > div > div > div {
        background-color: #198754;
    }


    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">🛡️ FinShield</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Credit Risk Assessment & Decision Support System'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="description">'
    'Assess customer credit risk using a trained XGBoost classification model.'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# LOAD MODEL
# ============================================================

@st.cache_resource
def load_model():

    return joblib.load(
        MODELS_DIR / "xgboost_model.pkl"
    )


# ============================================================
# LOAD FEATURE NAMES
# ============================================================

@st.cache_resource
def load_feature_names():

    return joblib.load(
        MODELS_DIR / "xgboost_features.pkl"
    )


# ============================================================
# LOAD CUSTOMER DATA
# ============================================================

@st.cache_data
def load_customer_data():
    return pd.read_csv(
        "data/final/clean_master_dataset.csv"
    )


model = load_model()

feature_names = load_feature_names()

customer_data = load_customer_data()


# ============================================================
# CUSTOMER SELECTION
# ============================================================

st.markdown(
    '<div class="section-title">👤 Customer Selection</div>',
    unsafe_allow_html=True
)

customer_id = st.number_input(
    "Enter Customer ID",
    min_value=int(customer_data["SK_ID_CURR"].min()),
    max_value=int(customer_data["SK_ID_CURR"].max()),
    step=1
)

customer = customer_data[
    customer_data["SK_ID_CURR"] == customer_id
].copy()

if customer.empty:

    st.warning(
        "⚠️ Customer ID not found. Please enter a valid Customer ID."
    )

    st.stop()
# ============================================================
# HELPER FUNCTION FOR INFO CARDS
# ============================================================

def info_card(label, value):

    st.markdown(
        f"""
        <div class="info-card">
            <div class="card-label">{label}</div>
            <div class="card-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# CUSTOMER PROFILE
# ============================================================

st.markdown(
    '<div class="section-title">👤 Customer Profile</div>',
    unsafe_allow_html=True
)

col1, col2, col3, col4 = st.columns(4)

with col1:

    gender = customer["CODE_GENDER"].iloc[0]

    gender_display = {
        "F": "Female",
        "M": "Male"
    }.get(gender, gender)

    info_card(
        "Gender",
        gender_display
    )


with col2:

    info_card(
        "Children",
        int(customer["CNT_CHILDREN"].iloc[0])
    )


with col3:

    info_card(
        "Family Members",
        int(customer["CNT_FAM_MEMBERS"].iloc[0])
    )


with col4:

    car = customer["FLAG_OWN_CAR"].iloc[0]

    car_display = {
        "Y": "Yes",
        "N": "No"
    }.get(car, car)

    info_card(
        "Owns Car",
        car_display
    )


st.write("")


col1, col2, col3, col4 = st.columns(4)

with col1:

    info_card(
        "Education",
        customer["NAME_EDUCATION_TYPE"].iloc[0]
    )


with col2:

    info_card(
        "Family Status",
        customer["NAME_FAMILY_STATUS"].iloc[0]
    )


with col3:

    info_card(
        "Housing",
        customer["NAME_HOUSING_TYPE"].iloc[0]
    )


with col4:

    info_card(
        "Income Type",
        customer["NAME_INCOME_TYPE"].iloc[0]
    )


# ============================================================
# FINANCIAL INFORMATION
# ============================================================

st.markdown(
    '<div class="section-title">💰 Financial Information</div>',
    unsafe_allow_html=True
)

col1, col2, col3, col4 = st.columns(4)

with col1:

    info_card(
        "Annual Income",
        f"₹{customer['AMT_INCOME_TOTAL'].iloc[0]:,.0f}"
    )


with col2:

    info_card(
        "Credit Amount",
        f"₹{customer['AMT_CREDIT'].iloc[0]:,.0f}"
    )


with col3:

    info_card(
        "Annuity",
        f"₹{customer['AMT_ANNUITY'].iloc[0]:,.0f}"
    )


with col4:

    info_card(
        "Goods Price",
        f"₹{customer['AMT_GOODS_PRICE'].iloc[0]:,.0f}"
    )


# ============================================================
# EMPLOYMENT & CREDIT PROFILE
# ============================================================

st.markdown(
    '<div class="section-title">💼 Employment & Credit Profile</div>',
    unsafe_allow_html=True
)

col1, col2, col3, col4 = st.columns(4)

with col1:

    info_card(
        "Occupation",
        customer["OCCUPATION_TYPE"].iloc[0]
    )


with col2:

    info_card(
        "Organization",
        customer["ORGANIZATION_TYPE"].iloc[0]
    )


with col3:

    score = customer["EXT_SOURCE_1"].iloc[0]

    info_card(
        "External Score 1",
        "Unavailable" if pd.isna(score) else f"{score:.3f}"
    )


with col4:

    score = customer["EXT_SOURCE_2"].iloc[0]

    info_card(
        "External Score 2",
        "Unavailable" if pd.isna(score) else f"{score:.3f}"
    )


st.write("")


col1, col2, col3, col4 = st.columns(4)

with col1:

    score = customer["EXT_SOURCE_3"].iloc[0]

    info_card(
        "External Score 3",
        "Unavailable" if pd.isna(score) else f"{score:.3f}"
    )


with col2:

    info_card(
        "Previous Credit Ratio",
        f"{customer['prev_credit_application_ratio'].iloc[0]:.2f}"
    )


with col3:

    info_card(
        "Previous Applications",
        f"{customer['prev_name_contract_status_approved'].iloc[0]:.0f}"
    )


with col4:

    info_card(
        "Bureau Loans",
        f"{customer['bureau_total_loans'].iloc[0]:.0f}"
    )

# ============================================================
# SHAP FEATURE DISPLAY NAMES
# ============================================================

SHAP_FEATURE_NAMES = {

    # --------------------------------------------------------
    # Application / Customer Features
    # --------------------------------------------------------

    "AMT_INCOME_TOTAL": "Total Annual Income",
    "AMT_CREDIT": "Loan Credit Amount",
    "AMT_ANNUITY": "Annual Loan Payment",
    "AMT_GOODS_PRICE": "Goods / Property Price",

    "DAYS_BIRTH": "Age of Customer",
    "DAYS_EMPLOYED": "Employment Duration",
    "DAYS_ID_PUBLISH": "ID Document Age",
    "DAYS_REGISTRATION": "Registration Duration",
    "DAYS_LAST_PHONE_CHANGE": "Time Since Phone Change",

    "CNT_CHILDREN": "Number of Children",
    "CNT_FAM_MEMBERS": "Family Size",

    "OWN_CAR_AGE": "Vehicle Age",
    "REGION_POPULATION_RELATIVE": "Region Population Density",

    # --------------------------------------------------------
    # External Credit Scores
    # --------------------------------------------------------

    "EXT_SOURCE_1": "External Credit Score 1",
    "EXT_SOURCE_2": "External Credit Score 2",
    "EXT_SOURCE_3": "External Credit Score 3",

    # --------------------------------------------------------
    # Gender
    # --------------------------------------------------------

    "CODE_GENDER_M": "Male Gender Indicator",
    "CODE_GENDER_F": "Female Gender Indicator",

    # --------------------------------------------------------
    # Education
    # --------------------------------------------------------

    "NAME_EDUCATION_TYPE_Higher education": "Higher Education",
    "NAME_EDUCATION_TYPE_Secondary / secondary special": "Secondary Education",
    "NAME_EDUCATION_TYPE_Incomplete higher": "Incomplete Higher Education",
    "NAME_EDUCATION_TYPE_Lower secondary": "Lower Secondary Education",
    "NAME_EDUCATION_TYPE_Academic degree": "Academic Degree",

    # --------------------------------------------------------
    # Family Status
    # --------------------------------------------------------

    "NAME_FAMILY_STATUS_Married": "Married Family Status",
    "NAME_FAMILY_STATUS_Single / not married": "Single Family Status",
    "NAME_FAMILY_STATUS_Civil marriage": "Civil Marriage Status",
    "NAME_FAMILY_STATUS_Separated": "Separated Family Status",
    "NAME_FAMILY_STATUS_Widow": "Widowed Family Status",

    # --------------------------------------------------------
    # Housing
    # --------------------------------------------------------

    "NAME_HOUSING_TYPE_House / apartment": "House / Apartment",
    "NAME_HOUSING_TYPE_With parents": "Living With Parents",
    "NAME_HOUSING_TYPE_Rented apartment": "Rented Apartment",
    "NAME_HOUSING_TYPE_Municipal apartment": "Municipal Apartment",
    "NAME_HOUSING_TYPE_Office apartment": "Office Apartment",
    "NAME_HOUSING_TYPE_Co-op apartment": "Cooperative Apartment",

    # --------------------------------------------------------
    # Loan / Credit Information
    # --------------------------------------------------------

    "NAME_CONTRACT_TYPE_Cash loans": "Cash Loan",
    "NAME_CONTRACT_TYPE_Revolving loans": "Revolving Loan",

    # --------------------------------------------------------
    # Bureau Features
    # --------------------------------------------------------

    "bureau_total_loans": "Total Previous Credit Accounts",
    "bureau_active_loans": "Active Previous Credit Accounts",
    "bureau_closed_loans": "Closed Previous Credit Accounts",
    "bureau_amt_credit_sum_mean": "Average Previous Credit Amount",
    "bureau_amt_credit_sum_median": "Median Previous Credit Amount",
    "bureau_amt_credit_sum_max": "Maximum Previous Credit Amount",
    "bureau_amt_credit_sum_min": "Minimum Previous Credit Amount",
    "bureau_debt_to_credit_ratio": "Previous Debt-to-Credit Ratio",

    # --------------------------------------------------------
    # Previous Application Features
    # --------------------------------------------------------

    "prev_credit_application_ratio": "Previous Credit-to-Application Ratio",
    "prev_annuity_credit_ratio": "Previous Annuity-to-Credit Ratio",
    "prev_amt_credit_mean": "Average Previous Credit Amount",
    "prev_amt_application_mean": "Average Previous Application Amount",
    "prev_amt_annuity_mean": "Average Previous Loan Payment",

    # --------------------------------------------------------
    # Installment Features
    # --------------------------------------------------------

    "installment_payment_mean": "Average Installment Payment",
    "installment_payment_sum": "Total Installment Payments",
    "installment_payment_max": "Maximum Installment Payment",
    "installment_days_entry_payment_mean": "Average Payment Timing",
    "installment_payment_delay_mean": "Average Payment Delay",

    # --------------------------------------------------------
    # POS Cash Features
    # --------------------------------------------------------

    "pos_months_balance_mean": "Average Account Duration",
    "pos_months_balance_min": "Minimum Account Duration",
    "pos_months_balance_max": "Maximum Account Duration",
    "pos_sk_dpd_mean": "Average Days Past Due",
    "pos_sk_dpd_max": "Maximum Days Past Due",
    "pos_sk_dpd_def_mean": "Average Severe Payment Delay",

    # --------------------------------------------------------
    # Credit Card Features
    # --------------------------------------------------------

    "cc_amt_balance_mean": "Average Credit Card Balance",
    "cc_amt_balance_max": "Maximum Credit Card Balance",
    "cc_amt_credit_limit_mean": "Average Credit Limit",
    "cc_amt_payment_total_mean": "Average Credit Card Payment",
    "cc_amt_payment_total_max": "Maximum Credit Card Payment",
    "cc_sk_dpd_mean": "Average Credit Card Days Past Due",
    "cc_sk_dpd_max": "Maximum Credit Card Days Past Due",
}

# ============================================================
# RISK ASSESSMENT
# ============================================================

st.divider()

st.markdown(
    '<div class="section-title">🔍 Risk Assessment</div>',
    unsafe_allow_html=True
)

assess_button = st.button(
    "🔍 Assess Credit Risk",
    use_container_width=True
)


if assess_button:

    # --------------------------------------------------------
    # Prepare the complete feature set
    # --------------------------------------------------------

    features = prepare_features(
        customer,
        feature_names
    )

    # --------------------------------------------------------
    # Generate prediction
    # --------------------------------------------------------

    probabilities, predictions = predict(
        model,
        features
    )

    probability = probabilities[0]
    prediction = predictions[0]

    probability_percent = probability * 100


    # --------------------------------------------------------
    # Determine dashboard risk level
    # --------------------------------------------------------

    if probability < 0.10:
        risk = "LOW RISK"
        risk_color = "#198754"
        risk_background = "#F3FAF6"
        risk_icon = "🟢"

    elif probability < 0.20:
        risk = "MEDIUM RISK"
        risk_color = "#E67E22"
        risk_background = "#FFF4E5"
        risk_icon = "🟠"

    else:
        risk = "HIGH RISK"
        risk_color = "#DC3545"
        risk_background = "#FDECEC"
        risk_icon = "🔴"

    risk_html = (
        f'<div style="padding:25px; '
        f'border:2px solid {risk_color}; '
        f'border-radius:12px; '
        f'background-color:{risk_background}; '
        f'text-align:center; '
        f'margin-top:15px;">'

        f'<div style="font-size:42px; '
        f'font-weight:700; '
        f'color:{risk_color};">'
        f'{probability_percent:.2f}%'
        f'</div>'

        f'<div style="font-size:14px; '
        f'color:#6C7A72;">'
        f'Default Probability'
        f'</div>'

        f'<div style="font-size:24px; '
        f'font-weight:700; '
        f'color:{risk_color}; '
        f'margin-top:12px;">'
        f'{risk_icon} {risk}'
        f'</div>'

        f'</div>'
    )

    st.markdown(
        risk_html,
        unsafe_allow_html=True
    )

    # --------------------------------------------------------
    # Prediction result
    # --------------------------------------------------------

    if prediction == 1:

        st.error(
            "⚠️ Prediction: DEFAULT"
        )

    else:

        st.success(
            "✅ Prediction: NON-DEFAULT"
        )

    # ============================================================
    # SHAP EXPLANATION
    # ============================================================

    st.markdown(
        '<div class="section-title">🧠 Why did FinShield make this prediction?</div>',
        unsafe_allow_html=True
    )

    with st.spinner("Generating model explanation..."):

        explanation = explain_customer(
            model,
            features
        )


    # ------------------------------------------------------------
    # Convert technical feature names into business-friendly names
    # ------------------------------------------------------------

    def get_display_name(feature_name):

        # Exact match
        if feature_name in SHAP_FEATURE_NAMES:
            return SHAP_FEATURE_NAMES[feature_name]

        # One-hot encoded family status
        if feature_name.startswith("NAME_FAMILY_STATUS_"):
            status = feature_name.replace(
                "NAME_FAMILY_STATUS_",
                ""
            )
            return f"{status} Family Status"

        # One-hot encoded education
        if feature_name.startswith("NAME_EDUCATION_TYPE_"):
            education = feature_name.replace(
                "NAME_EDUCATION_TYPE_",
                ""
            )
            return education

        # One-hot encoded housing
        if feature_name.startswith("NAME_HOUSING_TYPE_"):
            housing = feature_name.replace(
                "NAME_HOUSING_TYPE_",
                ""
            )
            return housing

        # One-hot encoded occupation
        if feature_name.startswith("OCCUPATION_TYPE_"):
            occupation = feature_name.replace(
                "OCCUPATION_TYPE_",
                ""
            )
            return f"{occupation} Occupation"

        # One-hot encoded contract type
        if feature_name.startswith("NAME_CONTRACT_TYPE_"):
            contract = feature_name.replace(
                "NAME_CONTRACT_TYPE_",
                ""
            )
            return f"{contract} Contract"

        # --------------------------------------------------------
        # Generic engineered feature formatting
        # --------------------------------------------------------

        display_name = feature_name

        display_name = display_name.replace(
            "bureau_",
            "Previous Credit: "
        )

        display_name = display_name.replace(
            "prev_",
            "Previous Application: "
        )

        display_name = display_name.replace(
            "installment_",
            "Installment: "
        )

        display_name = display_name.replace(
            "pos_",
            "POS Cash: "
        )

        display_name = display_name.replace(
            "cc_",
            "Credit Card: "
        )

        display_name = display_name.replace(
            "_",
            " "
        )

        return display_name.title()


    # Add business-friendly name to explanation dataframe

    explanation["display_name"] = explanation["feature"].apply(
        get_display_name
    )


    # ------------------------------------------------------------
    # Separate positive and negative SHAP factors
    # ------------------------------------------------------------

    positive_factors = explanation[
        explanation["shap_value"] > 0
    ].head(5)

    negative_factors = explanation[
        explanation["shap_value"] < 0
    ].sort_values(
        "shap_value"
    ).head(5)


    # ============================================================
    # DISPLAY SHAP FACTORS
    # ============================================================

    col1, col2 = st.columns(2)


    # ------------------------------------------------------------
    # Factors Increasing Risk
    # ------------------------------------------------------------

    with col1:

        st.subheader("⚠️ Factors Increasing Risk")

        if len(positive_factors) == 0:

            st.info(
                "No significant factors increasing default risk."
            )

        else:

            for _, row in positive_factors.iterrows():

                st.write(
                    f"**{row['display_name']}**"
                )

                st.progress(
                    min(
                        float(abs(row["shap_value"])) / 0.5,
                        1.0
                    )
                )

                st.caption(
                    f"Model impact: +{row['shap_value']:.4f}"
                )


    # ------------------------------------------------------------
    # Factors Reducing Risk
    # ------------------------------------------------------------

    with col2:

        st.subheader("🛡️ Factors Reducing Risk")

        if len(negative_factors) == 0:

            st.info(
                "No significant factors reducing default risk."
            )

        else:

            for _, row in negative_factors.iterrows():

                st.write(
                    f"**{row['display_name']}**"
                )

                st.progress(
                    min(
                        float(abs(row["shap_value"])) / 0.5,
                        1.0
                    )
                )

                st.caption(
                    f"Model impact: {row['shap_value']:.4f}"
                )


    # ------------------------------------------------------------
    # SHAP Interpretation Note
    # ------------------------------------------------------------

    st.caption(
        "SHAP values show how each factor influenced the model's "
        "prediction. Positive values increase the model's estimated "
        "default risk, while negative values reduce it. "
        "These values represent model influence, not causation."
    )