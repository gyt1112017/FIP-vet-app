import streamlit as st

# ---- Custom Styles ----
st.markdown("""
<style>

.st-emotion-cache-ocsh0s:hover {
    border-color: #9b26b6 !important;
    color: #9b26b6 !important;
}

""", unsafe_allow_html=True)

# ---- Title ----
st.title("FIP Vet Companion Tool")

# Navigation menu in the sidebar
st.sidebar.title("📱 FIP Vet App")
page = st.sidebar.radio("Go to:", ["Diagnosis Guide", "Dose Calculator", "Case Tracker", "Request Advice", "FIP Learning Hub" ])
st.sidebar.markdown("---")
st.sidebar.markdown("### 💬 Need help or support?")
st.sidebar.markdown(
    """
    <a href="https://bova.vet/bova-uk/contact-us/" target="_blank">
        <button style='background-color:#9b26b6; color:white; border:none; border-radius:25px; padding:10px 20px; font-size:16px; width:100%;'>
            📩 Contact Us
        </button>
    </a>
    """,
    unsafe_allow_html=True
)
# Page: Diagnosis Guide
if page == "Diagnosis Guide":
    st.title("🧪 FIP Diagnosis Guide")

    # Step 1
    st.markdown("### 1. Signalment & History")
    age = st.radio("Is the cat under 2 years old?", ["Yes", "No"])
    breed = st.radio("Is it a pedigree breed (e.g. Ragdoll, Bengal, Abyssinian)?", ["Yes", "No"])
    environment = st.radio("Recent stress or multi-cat environment?", ["Yes", "No"])
    risk_score = sum([age == "Yes", breed == "Yes", environment == "Yes"])

    # Step 2
    st.markdown("### 2. Clinical Signs")
    signs = st.multiselect("Which signs are present?", [
        "Weight loss", "Persistent fever", "Abdominal distension (ascites)",
        "Dyspnoea (pleural effusion)", "Icterus",
        "Ocular involvement", "Neurological signs"
    ])

    # Step 3
    st.markdown("### 3. Effusion Status")
    effusion = st.radio("Is there abdominal or thoracic effusion?", ["Yes", "No", "Unknown"])

    # Step 4
    st.markdown("### 4. Diagnostic Tests")
    tests = st.multiselect("Which diagnostics have been run?", [
        "CBC/Biochem", "A:G ratio < 0.4", "FCoV titre",
        "Effusion Rivalta test", "Effusion cytology",
        "RT-PCR (fluid or tissue)", "None yet"
    ])

    # Outcome
    st.markdown("### 🧠 Suggested Interpretation")
    if "RT-PCR (fluid or tissue)" in tests:
        st.success("✅ Positive RT-PCR – Diagnosis supported. Cascade justification strong.")
    elif "A:G ratio < 0.4" in tests and len(signs) >= 2:
        st.success("🧠 Strong suspicion of FIP based on clinical signs + A:G ratio.")
    elif risk_score >= 2 and len(signs) >= 3:
        st.warning("⚠️ Suspicion moderate to high. Recommend diagnostics or treatment trial.")
    else:
        st.info("ℹ️ FIP less likely. Recommend further diagnostics or alternative diagnosis.")


# Page: Dose Calculator
elif page == "Dose Calculator":
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

elif page == "Case Tracker":
    import pandas as pd
    import streamlit as st
    from datetime import datetime

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



# Page: Request Advice
elif page == "Request Advice":
    st.title("📩 Request FIP Case Advice")

    with st.form("advice_form"):
        name = st.text_input("Your Name")
        practice = st.text_input("Practice Name")
        email = st.text_input("Email Address")
        notes = st.text_area("Case Summary / Questions")

        submitted = st.form_submit_button("Submit Advice Request")
        if submitted:
            st.success("✅ Thank you! A team member will be in touch shortly.")

elif page == "FIP Learning Hub":
    st.title("🎓 FIP Learning Hub")

    st.markdown("Discover our latest FIP CPD resources:")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div style="border:2px solid #9b26b6; border-radius:15px; padding:1rem; margin-bottom:1rem;">
            <h4 style="color:#9b26b6;">🎥 FIP On-demand Webinars</h4>
            <p>Get confident with diagnosing FIP in first opinion practice.</p>
            <a href="https://bova.vet/tag/feline-infectious-peritonitis/" target="_blank" style="color:#9b26b6; text-decoration:none; font-weight:bold;">
                🔗 Explore more
            </a>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style="border:2px solid #9b26b6; border-radius:15px; padding:1rem;">
            <h4 style="color:#9b26b6;">🎧 FIP Podcasts</h4>
            <p>Discussing treatment, owner communication, and real-world experiences.</p>
            <a href="https://yourpodcastlink.com" target="_blank" style="color:#9b26b6; text-decoration:none; font-weight:bold;">
                🎧 Listen Now
            </a>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style="border:2px solid #9b26b6; border-radius:15px; padding:1rem; margin-bottom:1rem;">
            <h4 style="color:#9b26b6;">📖 FIP Blogs </h4>
            <p>The treatment of feline infectious peritonitis (FIP) in the UK– an update FIP treatment protocols – what’s new?</p>
            <a href="https://bova.vet/2023/08/10/fip-an-update/" target="_blank" style="color:#9b26b6; text-decoration:none; font-weight:bold;">
                📚 Read Blog
            </a>
        </div>
        """, unsafe_allow_html=True)


# ---- Footer ----
st.markdown("---")
st.caption("@Bova 2025. For veterinary professionals only. This app is for clinical support and educational use.")
