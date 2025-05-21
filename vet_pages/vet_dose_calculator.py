# Page: Dose Calculator
import streamlit as st
def show():
    st.title("Dose Calculator")

    # Input
    weight = st.number_input("Patient weight (kg)", min_value=0.1, step=0.1)
    dosage_rate = st.number_input("Dosage rate (mg/kg)", min_value=0.1, step=0.1)
    route = st.radio("Route of administration", ["Oral tablet", "Oral liquid", "Injectable"])
    strength = st.number_input("Medication concentration", min_value=0.1, step=0.1)
    duration_days = st.number_input("Treatment duration (days)", value=84)


    # Calculate
    if st.button("Calculate Dose"):
        daily_dose_mg = round(weight * dosage_rate, 2)
        total_dose_mg = round(daily_dose_mg * duration_days, 2)
        daily_volume_ml = round(daily_dose_mg / strength, 2)
        total_volume_ml = round(total_dose_mg / strength, 2)

        st.markdown("### Dosing Summary")
        st.success(f"""
        **Daily Dose:** {daily_dose_mg} mg  
        **Daily Volume Required:** {daily_volume_ml} ml  
        **Total Dose (for {duration_days} days):** {total_dose_mg} mg  
        **Total Volume Required:** {total_volume_ml} ml
        """)
