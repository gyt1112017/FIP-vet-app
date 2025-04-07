# Page: Dose Calculator
import streamlit as st
def show():
    st.title("💊 Dose Calculator")

    # Input
    weight = st.number_input("Patient weight (kg)", min_value=0.1, step=0.1)
    dosage_rate = st.selectbox("Dosage rate (mg/kg/day)", [4, 5, 6])  # Could be 4–6 mg/kg for FIP
    route = st.radio("Route of administration", ["Oral", "Injectable"])
    form_strength = st.selectbox("Medication concentration", ["15 mg/ml", "20 mg/ml", "Custom"])
    duration_days = st.number_input("Treatment duration (days)", value=84)

    # Optional: custom strength
    if form_strength == "Custom":
        strength = st.number_input("Enter concentration (mg/ml)", value=20.0, step=0.5)
    else:
        strength = float(form_strength.split(" ")[0])

    # Calculate
    if st.button("Calculate Dose"):
        daily_dose_mg = round(weight * dosage_rate, 2)
        total_dose_mg = round(daily_dose_mg * duration_days, 2)
        daily_volume_ml = round(daily_dose_mg / strength, 2)
        total_volume_ml = round(total_dose_mg / strength, 2)

        st.markdown("### 💊 Dosing Summary")
        st.success(f"""
        **Daily Dose:** {daily_dose_mg} mg  
        **Daily Volume Required:** {daily_volume_ml} ml  
        **Total Dose (for {duration_days} days):** {total_dose_mg} mg  
        **Total Volume Required:** {total_volume_ml} ml
        """)

        # Optional caution
        if daily_volume_ml > 5:
            st.warning("⚠️ Daily volume seems high. Please double-check formulation or dose rate.")