import streamlit as st
import pandas as pd
import pickle
import os
import time
import db_manager

# =========================================================
#  0. CONFIGURATION & STYLING
# =========================================================
st.set_page_config(
    page_title="MetaboTwin AI", 
    layout="wide", 
    page_icon="🧬",
    initial_sidebar_state="collapsed"
)

# Professional Styling
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .big-font {
        font-size:40px !important;
        font-weight: 700;
        color: #2E86C1;
        text-align: center;
    }
    .sub-font {
        font-size:18px !important;
        color: #566573;
        text-align: center;
        margin-bottom: 20px;
    }
    .stButton button {
        border-radius: 8px;
        height: 3em;
    }
    </style>
    """, unsafe_allow_html=True)

# --- LOAD BRAIN ---
model_path = os.path.join('Models', 'twin_brain.pkl')
if not os.path.exists(model_path):
    st.error("Brain not found! Please run 'TrainModel.py' first.")
    st.stop()

with open(model_path, 'rb') as f:
    model = pickle.load(f)

db_manager.init_db()

# --- HELPER: BMI CALCULATOR ---
def calculate_bmi(weight, weight_unit, height, height_unit):
    if weight_unit == "Lbs": weight_kg = weight * 0.453592
    else: weight_kg = weight

    if height_unit == "Cm": height_m = height / 100
    elif height_unit == "Inches": height_m = height * 0.0254
    elif height_unit == "Feet": height_m = height * 0.3048
    else: height_m = height

    return weight_kg / (height_m ** 2) if height_m > 0 else 0

# --- SESSION STATE ---
if 'step' not in st.session_state: st.session_state['step'] = 1
if 'user_data' not in st.session_state: st.session_state['user_data'] = {}

# =========================================================
#  STEP 1: PATIENT CHECK-IN
# =========================================================
if st.session_state['step'] == 1:
    st.write("##")
    st.markdown('<p class="big-font">🏥 MetaboTwin Check-In</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-font">AI-Powered Metabolic Health Simulator</p>', unsafe_allow_html=True)
    st.divider()

    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        with st.container(border=True):
            st.markdown("### 👤 Patient Identity")
            p_name = st.text_input("Full Name", placeholder="e.g. Srishti Bhatia")
            p_id = st.text_input("Patient ID (Optional)", placeholder="e.g. PAT-2025-X")
            
            st.write("##")
            if st.button("Next: Calibration ➡️", type="primary", use_container_width=True):
                if p_name.strip() == "":
                    st.toast("⚠️ Please enter a name to continue.")
                else:
                    st.session_state['user_data']['name'] = p_name
                    st.session_state['user_data']['id'] = p_id if p_id else "Guest"
                    st.session_state['step'] = 2
                    st.rerun()

# =========================================================
#  STEP 2: GENDER SELECTION
# =========================================================
elif st.session_state['step'] == 2:
    st.write("##")
    st.markdown('<p class="big-font">🧬 System Calibration</p>', unsafe_allow_html=True)
    st.progress(33, text="Step 2 of 4: Biological Context")
    
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        st.info(f"Welcome, **{st.session_state['user_data']['name']}**. Select biological gender to load medical protocols.")
        
        with st.container(border=True):
            st.markdown("### Select Gender")
            gender = st.radio("", ["Male", "Female"], horizontal=True, label_visibility="collapsed")
            
            st.write("##")
            col_b1, col_b2 = st.columns(2)
            with col_b1:
                if st.button("⬅️ Back", use_container_width=True):
                    st.session_state['step'] = 1
                    st.rerun()
            with col_b2:
                if st.button("Next: Vitals ➡️", type="primary", use_container_width=True):
                    st.session_state['user_data']['gender'] = gender
                    st.session_state['step'] = 3
                    st.rerun()

# =========================================================
#  STEP 3: MEDICAL INTAKE (LIVE FORM)
# =========================================================
elif st.session_state['step'] == 3:
    gender = st.session_state['user_data']['gender']
    name = st.session_state['user_data']['name']
    
    st.markdown(f"## 📝 Clinical Profile: {name}")
    st.progress(66, text="Step 3 of 4: Full Medical Intake")
    
    layout_col1, layout_col2, layout_col3 = st.columns([1, 2, 1])
    
    with layout_col2:
        # --- 1. VITALS ---
        st.markdown("### 🩺 1. Biometrics")
        age = st.number_input("Age (Years)", 1, 100, 25)
        
        w_col1, w_col2 = st.columns([3, 1]) 
        with w_col1: weight_val = st.number_input("Weight", value=70.0)
        with w_col2: weight_unit = st.selectbox("Unit", ["Kg", "Lbs"], key="w_u")
        
        h_col1, h_col2 = st.columns([3, 1])
        with h_col1: height_val = st.number_input("Height", value=170.0)
        with h_col2: height_unit = st.selectbox("Unit", ["Cm", "Feet", "Inches"], key="h_u")

        st.divider()

        # --- 2. MEDICAL HISTORY ---
        st.markdown("### 🧪 2. Medical History")
        bp_val = st.number_input("Diastolic BP (Bottom Number)", value=72, help="Ideal <80")
        glucose_val = st.number_input("Fasting Glucose (mg/dL)", value=100, help="Ideal <100")
        
        st.write("##")
        st.caption("Current Conditions")
        on_meds = st.radio("Taking Medication?", ["No", "Yes"], horizontal=True)
        is_sick = st.radio("Currently Sick?", ["No", "Yes"], horizontal=True)

        st.divider()

        # --- 3. LIFESTYLE ---
        st.markdown("### 🏃 3. Lifestyle")
        activity = st.selectbox("Activity Level", 
                                ["Sedentary (No Exercise)", "Lightly Active", "Moderately Active", "Very Active"])
        smoking = st.radio("Smoking Status", ["No", "Yes", "Former Smoker"], horizontal=True)
        sleep = st.slider("Nightly Sleep (Hours)", 3, 12, 7)

        st.divider()

        # --- 4. GENETICS (EXPANDED) ---
        st.markdown("### 🧬 4. Family History")
        st.caption("Select conditions present in immediate family (Parents/Siblings):")
        
        g_c1, g_c2, g_c3 = st.columns(3)
        with g_c1:
            fam_diabetes = st.checkbox("Diabetes (Type 1 or 2)")
            fam_bp = st.checkbox("High Blood Pressure")
        with g_c2:
            fam_heart = st.checkbox("Heart Disease / Stroke")
            fam_obesity = st.checkbox("Severe Obesity")
        with g_c3: 
            fam_none = st.checkbox("None")

        # --- 5. FEMALE METRICS (CONDITIONAL) ---
        pregnancies = 0
        menopause = "No"
        
        if gender == "Female":
            st.divider()
            st.markdown("### 👩 Female Metrics")
            with st.container(border=True):
                # Live Logic for Pregnancy
                is_pregnant = st.radio("Have you ever been pregnant?", ["No", "Yes"], horizontal=True)
                if is_pregnant == "Yes":
                    pregnancies = st.number_input("Count of full-term pregnancies", 1, 15, 1)
                
                st.write("---")
                menopause = st.radio("Have you reached menopause?", ["No", "Yes"], horizontal=True)

        st.write("##")
        
        # NAVIGATION
        c_nav1, c_nav2 = st.columns(2)
        with c_nav1:
            if st.button("⬅️ Back", use_container_width=True):
                st.session_state['step'] = 2
                st.rerun()
        with c_nav2:
            if st.button("🚀 Run Simulation", type="primary", use_container_width=True):
                with st.spinner("🔄 Generating Digital Twin..."):
                    time.sleep(1.0)
                    calculated_bmi = calculate_bmi(weight_val, weight_unit, height_val, height_unit)
                    
                    # Store everything
                    st.session_state['user_data'].update({
                        'age': age, 'bmi': calculated_bmi,
                        'bp': bp_val, 'glucose': glucose_val, 
                        'fam_diabetes': fam_diabetes, 'fam_bp': fam_bp,
                        'fam_heart': fam_heart, 'fam_obesity': fam_obesity,
                        'pregnancies': pregnancies, 'menopause': menopause,
                        'activity': activity, 'smoking': smoking, 'sleep': sleep,
                        'on_meds': on_meds, 'is_sick': is_sick
                    })
                    st.session_state['step'] = 4
                    st.rerun()

# =========================================================
#  STEP 4: DASHBOARD & RESULTS
# =========================================================
elif st.session_state['step'] == 4:
    user = st.session_state['user_data']
    
    # --- LOGIC LAYER: CALCULATING RISK ---
    
    # 1. Genetic Risk (Additive Logic)
    # Base starts low
    dpf = 0.1 
    if user['fam_diabetes']: dpf += 0.6  # High impact
    if user['fam_bp']:       dpf += 0.2
    if user['fam_heart']:    dpf += 0.2
    if user['fam_obesity']:  dpf += 0.2
    dpf = min(dpf, 2.0) # Cap at 2.0
    
    # 2. Lifestyle Modifiers
    lifestyle_factor = 0.0
    if user['activity'] == "Sedentary (No Exercise)": lifestyle_factor += 0.05 
    if user['activity'] == "Very Active": lifestyle_factor -= 0.05
    if user['smoking'] == "Yes": lifestyle_factor += 0.10
    if user['sleep'] < 6: lifestyle_factor += 0.05
    
    # --- DASHBOARD HEADER ---
    c_h1, c_h2 = st.columns([3, 1])
    with c_h1:
        st.title(f"🧬 Patient: {user['name']}")
        st.caption(f"ID: {user['id']} | Gender: {user['gender']} | Age: {user['age']}")
    with c_h2:
        if st.button("🔄 New Patient"):
            st.session_state['step'] = 1
            st.rerun()
    st.divider()

    col1, col2 = st.columns([1, 2])
    
    # --- LEFT: SIMULATOR CONTROLS ---
    with col1:
        st.subheader("⚙️ Twin Controls")
        with st.container(border=True):
            st.info("Adjust values to simulate improvements.")
            glucose = st.slider("🩸 Glucose", 50, 200, int(user['glucose']))
            bmi = st.slider("⚖️ BMI", 10.0, 50.0, float(user['bmi']))
            bp = st.slider("💓 Diastolic BP", 40, 140, int(user['bp']))
            
            # Prediction
            input_data = pd.DataFrame([[user['pregnancies'], glucose, bp, 20, 80, bmi, dpf, user['age']]],
                                      columns=['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age'])
            base_prob = model.predict_proba(input_data)[0][1]
            final_prob = min(max(base_prob + lifestyle_factor, 0), 1)

            st.write("##")
            if st.button("💾 Save to History", use_container_width=True):
                db_manager.add_log(glucose, bmi, user['age'], final_prob)
                st.toast("✅ Saved to database!", icon="💾")

    # --- RIGHT: ANALYTICS ---
    with col2:
        st.subheader("📊 Clinical Analysis")
        
        # Metrics
        m1, m2, m3 = st.columns(3)
        with m1: st.metric("Total Risk Score", f"{final_prob*100:.1f}%", f"{lifestyle_factor*100:+.1f}% Lifestyle", delta_color="inverse")
        with m2: st.metric("Biological Risk", f"{base_prob*100:.1f}%", help="Based on Vitals + Genetics")
        with m3: 
            status = "Healthy" if final_prob < 0.5 else "At Risk"
            st.metric("Risk Status", status)

        # Alerts
        if user['smoking'] == "Yes": 
            st.error("⚠️ **CRITICAL:** Smoking adds +10% risk penalty.")
        if user.get('menopause') == "Yes":
            st.info("ℹ️ Menopause context applied to metabolic rate.")

        # Graph
        st.markdown("### 🔮 Outcome Simulation")
        st.caption("Projected risk reduction if Glucose levels are managed:")
        
        sim_data = []
        for g in range(80, 200, 5):
            temp_df = input_data.copy()
            temp_df['Glucose'] = g
            p = model.predict_proba(temp_df)[0][1] + lifestyle_factor
            sim_data.append(min(p, 1))
            
        chart_data = pd.DataFrame({'Glucose': range(80, 200, 5), 'Risk': sim_data})
        st.line_chart(chart_data.set_index('Glucose'), color="#FF4B4B")

        # History
        with st.expander("📜 View Patient History"):
            st.dataframe(db_manager.get_history(), use_container_width=True)