import pandas as pd
import streamlit as st
from datetime import datetime
def show():
    st.title("📂 FIP Case Tracker")

    # ----- Case Submission Form -----
    st.markdown("### 📋 Submit New Case")

    with st.form("case_form"):
        case_id = st.text_input("Case ID or Patient Name")
        email = st.text_input("Vet Email")
        start_date = st.date_input("Treatment Start Date")
        diagnosis_type = st.radio("Diagnosis Form", ["Wet", "Dry", "Unclear"])
        initial_weight = st.number_input("Initial Weight (kg)", min_value=0.1, step=0.1)
        notes = st.text_area("Case Notes / Response")
        submit_case = st.form_submit_button("📥 Save Case")

        if submit_case:
            with open("fip_cases.csv", "a") as f:
                f.write(f"{case_id},{email},{start_date},{diagnosis_type},{initial_weight},{notes}\n")
            st.success(f"✅ Case '{case_id}' saved!")

    # ----- Vet-Specific Case Dashboard -----
    st.markdown("---")
    st.markdown("### 🔍 View My Submitted Cases")

    user_email = st.text_input("Enter your email to view your submitted cases:")

    try:
        df = pd.read_csv("fip_cases.csv", names=["Patient", "Email", "Start Date", "Form", "Weight (kg)", "Notes"])
        df["Start Date"] = pd.to_datetime(df["Start Date"], errors='coerce')

        if user_email:
            vet_df = df[df["Email"].str.lower() == user_email.lower()]
            if not vet_df.empty:
                st.success(f"Showing {len(vet_df)} case(s) for {user_email}")
                st.dataframe(vet_df)

                # Optional summary
                st.markdown("#### 📈 Summary")
                st.metric("Total Cases", len(vet_df))
                st.metric("Average Weight", f"{vet_df['Weight (kg)'].mean():.2f} kg")
            else:
                st.info("No cases found for this email.")
    except FileNotFoundError:
        st.warning("No case data found. Please submit a case to begin tracking.")
