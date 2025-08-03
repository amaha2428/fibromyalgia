import streamlit as st
import joblib
import pandas as pd
import os
from datetime import date

# Load model with error handling
MODEL_PATH = "voting_classifier_model.pkl"
if not os.path.exists(MODEL_PATH):
    st.error(f"Model file '{MODEL_PATH}' not found. Please ensure it is in the app directory.")
    st.stop()

with open(MODEL_PATH, "rb") as f:
    model = joblib.load(f)

# Page setup
st.set_page_config(
    page_title="Fibromyalgia Detection",
    layout="wide",
    page_icon="🧠",
    initial_sidebar_state="expanded"
)

# Sidebar with info
with st.sidebar:
    st.image("https://fibromyalgiaaustralia.org.au/wp-content/uploads/Pain-all-over-1024x1024.jpg", use_column_width=True)
    st.markdown("""
    # Fibromyalgia Detection
    This tool helps clinicians and patients assess the likelihood of Fibromyalgia using clinical, demographic, and physiological data.
    
    **Instructions:**
    - Fill in the information step by step.
    - Click **Next** to proceed, **Back** to review, and **Submit & Predict** to get results.
    
    _For medical use only. Consult a healthcare professional for diagnosis._
    """)

st.markdown("""
    <style>
    .stApp {background-color: #f7fafd;}
    .block-container {padding-top: 2rem;}
    .stButton>button {background-color: #4f8bf9; color: white; font-weight: bold;}
    .stSuccess {background-color: #e0f7fa;}
    </style>
    """, unsafe_allow_html=True)

st.title("🧠 Fibromyalgia Detection System")

if 'page' not in st.session_state:
    st.session_state.page = 0

# Initialize user input in session state
if 'user_input' not in st.session_state:
    st.session_state.user_input = {}

user_input = st.session_state.user_input

def go_next():
    st.session_state.page += 1

def go_back():
    st.session_state.page -= 1

def go_start():
    st.session_state.page = 0

if st.session_state.page == 0:
    st.header("1️⃣ Demographic Information")

    user_input['age'] = st.number_input("Age", min_value=0, max_value=120, step=1, value=user_input.get('age', 0))
    user_input['marital_status'] = st.selectbox(
        "Marital Status",
        [1, 2, 3, 4],
        format_func=lambda x: {
            1: "Single", 
            2: "Married/Cohabitating", 
            3: "Separated/Divorced", 
            4: "Widow"
        }[x],
        index=user_input.get('marital_status', 1)-1 if user_input.get('marital_status') else 0
    )
    user_input['occupational_pattern'] = st.selectbox(
        "Occupational Pattern", 
        [1, 2, 3, 4, 5, 6, 7, 8, 9], 
        format_func=lambda x: {
            1: "Professional/Executive", 
            2: "Business", 
            3: "Technician", 
            4: "Laborer", 
            5: "Housewife", 
            6: "Student", 
            7: "Pensioned", 
            8: "Unemployed", 
            9: "Other"
        }[x],
        index=user_input.get('occupational_pattern', 1)-1 if user_input.get('occupational_pattern') else 0
    )
    user_input['monthly_income'] = st.number_input("Monthly Income ", min_value=0, value=user_input.get('monthly_income', 0))

    # Navigation buttons at the bottom
    col1, col2 = st.columns([1, 1])
    with col2:
        st.button("Next", on_click=go_next, key="next0")

elif st.session_state.page == 1:
    st.header("2️⃣ Health & Clinical Info")

    user_input['substance_usage_disorder'] = st.radio(
        "Substance/Alcohol Use Disorder?", [0, 1],
        format_func=lambda x: "Yes" if x else "No",
        index=user_input.get('substance_usage_disorder', 0)
    )
    user_input['suicide_self_harm'] = st.radio(
        "History of Suicide or Self-Harm?", [0, 1],
        format_func=lambda x: "Yes" if x else "No",
        index=user_input.get('suicide_self_harm', 0)
    )
    user_input['pain_intensity'] = st.selectbox(
        "Pain Intensity", [-1, 0, 1],
        format_func=lambda x: { -1: "Low", 0: "Moderate", 1: "High" }[x],
        index=[-1, 0, 1].index(user_input.get('pain_intensity', -1))
    )
    user_input['total_widespread_index'] = st.slider(
        "Widespread Pain Index (0–19)", 0, 19, value=user_input.get('total_widespread_index', 0)
    )
    user_input['symptoms_experienced'] = st.slider(
        "No. of Symptoms Experienced (0–41)", 0, 41, value=user_input.get('symptoms_experienced', 0)
    )
    user_input['sss_severity_score'] = st.slider(
        "SSS Severity Score (0–12)", 0, 12, value=user_input.get('sss_severity_score', 0)
    )
    user_input['resting_fmri_done'] = st.radio(
        "Resting fMRI Done?", [0, 1],
        format_func=lambda x: "Yes" if x else "No",
        index=user_input.get('resting_fmri_done', 0)
    )
    user_input['comorb_presence'] = st.radio(
        "Comorbidity Present?", [0, 1],
        format_func=lambda x: "Yes" if x else "No",
        index=user_input.get('comorb_presence', 0)
    )

    # Navigation buttons at the bottom
    col1, col2 = st.columns([1, 1])
    with col1:
        st.button("Back", on_click=go_back, key="back1")
    with col2:
        st.button("Next", on_click=go_next, key="next1")

elif st.session_state.page == 2:
    st.header("3️⃣ Medication & Physiological Metrics")

    user_input['number_drugs_currently'] = st.slider(
        "No. of Drugs Used Daily", 0, 15, value=user_input.get('number_drugs_currently', 0)
    )
    user_input['number_drugs_crisis'] = st.slider(
        "No. of Drugs Used During Crisis", 0, 20, value=user_input.get('number_drugs_crisis', 0)
    )
    user_input['daily_dose'] = st.number_input(
        "Daily Dose (Opioids)", min_value=0.0, value=user_input.get('daily_dose', 0.0)
    )
    user_input['menstrual_cycle_duration'] = st.number_input(
        "Menstrual Cycle Duration (days)", min_value=-1.0, value=user_input.get('menstrual_cycle_duration', -1.0)
    )
    user_input['menstrual_cycle_regular'] = st.selectbox(
        "Cycle Regularity", [-1.0, 1.0, 2.0],
        format_func=lambda x: { -1.0: "Not Applicable", 1.0: "Regular", 2.0: "Irregular" }[x],
        index=[-1.0, 1.0, 2.0].index(user_input.get('menstrual_cycle_regular', -1.0))
    )
    user_input['patient_weight'] = st.number_input(
        "Weight (kg)", min_value=0.0, value=user_input.get('patient_weight', 0.0)
    )
    user_input['patient_height'] = st.number_input(
        "Height (cm)", min_value=0, value=user_input.get('patient_height', 0)
    )
    user_input['bmi'] = st.number_input(
        "BMI", min_value=0.0, value=user_input.get('bmi', 0.0)
    )
    user_input['imd'] = st.number_input(
        "Daily Morphine Dose (IMD)", min_value=0.0, value=user_input.get('imd', 0.0)
    )
    # Days Since Last Menstrual as date input
    last_menstrual_date = st.date_input(
        "Date of Last Menstrual Period",
        value=user_input.get('last_menstrual_date', date.today()),
        min_value=date(1900, 1, 1),
        max_value=date.today()
    )
    user_input['last_menstrual_date'] = last_menstrual_date
    # Calculate days since last menstrual
    days_since_last_menstrual = (date.today() - last_menstrual_date).days if last_menstrual_date else -1
    user_input['days_since_last_menstrual'] = days_since_last_menstrual
    st.info(f"Days Since Last Menstrual: {days_since_last_menstrual}")

    # Navigation buttons at the bottom
    col1, col2 = st.columns([1, 1])
    with col1:
        st.button("Back", on_click=go_back, key="back2")
    with col2:
        st.button("Submit & Predict", on_click=go_next, key="next2")

elif st.session_state.page == 3:
    st.header("🧪 Model Detection")
    st.markdown("---")

    # Ensure feature order matches model training
    feature_order = [
        'age', 'marital_status', 'occupational_pattern', 'monthly_income',
        'substance_usage_disorder', 'suicide_self_harm', 'pain_intensity',
        'total_widespread_index', 'symptoms_experienced', 'sss_severity_score',
        'resting_fmri_done', 'comorb_presence', 'number_drugs_currently',
        'number_drugs_crisis', 'daily_dose', 'menstrual_cycle_duration',
        'menstrual_cycle_regular', 'patient_weight', 'patient_height',
        'bmi', 'imd', 'days_since_last_menstrual'
    ]
    input_df = pd.DataFrame([[user_input.get(f, 0) for f in feature_order]], columns=feature_order)
    prediction = model.predict(input_df)[0]
    prediction_label = "Fibromyalgia" if prediction == 0 else "Healthy Control"

    st.markdown(f"""
    <div style='background-color:#e0f7fa;padding:1.2em 1em 1.2em 1em;border-radius:8px;margin-bottom:1em;'>
        🧬 <span style='color:#1976d2;font-size:1.5em;'>Predicted Class: <b>{prediction_label}</b></span>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("🔍 Input Summary")
    with st.expander("Show Input Details"):
        st.json(user_input)

    st.button("Start Over", on_click=go_start, key="startover")