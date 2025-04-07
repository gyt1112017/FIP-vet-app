import streamlit as st
from utils.styling import apply_theme
apply_theme()
from pages import vet_diagnosis, vet_dose_calculator, vet_case_tracker, vet_advice_form, vet_learning


# Ensure rerun works across all Streamlit versions
rerun = st.rerun if hasattr(st, "rerun") else st.experimental_rerun

# --- Landing Page ---
if "user_type" not in st.session_state:
    st.session_state.user_type = None

if st.session_state.user_type is None:
    st.title("Welcome to the FIP Companion App")
    st.markdown("Are you a:")
    choice = st.radio("Select user type", ["Veterinary Professional", "Pet Owner"])
    if st.button("Continue"):
        st.session_state.user_type = choice
        rerun()

# --- Navigation & Page Routing ---
elif st.session_state.user_type == "Veterinary Professional":
    page = st.sidebar.radio("Vet Menu", [
        "Diagnosis Guide",
        "Dose Calculator",
        "Case Tracker",
        "Advice Form",
        "FIP Learning Hub"
    ])

    if page == "Diagnosis Guide":
        vet_diagnosis.show()
    elif page == "Dose Calculator":
        vet_dose_calculator.show()
    elif page == "Case Tracker":
        vet_case_tracker.show()
    elif page == "Advice Form":
        vet_advice_form.show()
    elif page == "FIP Learning Hub":
        vet_learning.show()

elif st.session_state.user_type == "Pet Owner":
    page = st.sidebar.radio("Pet Owner Menu", [
        "FIP Overview",
        "FAQs",
        "Support Resources"
    ])

    if page == "FIP Overview":
        pet_overview.show()
    elif page == "FAQs":
        pet_faq.show()
    elif page == "Support Resources":
        pet_support.show()

# --- Shared Contact Button ---
st.sidebar.markdown("---")
st.sidebar.markdown("### ✨ Need help?")
st.sidebar.markdown("""
<a href="https://bova.vet/bova-uk/contact-us/" target="_blank">
    <button class="custom-contact-button">📩 Contact Us</button>
</a>
""", unsafe_allow_html=True)

# Option to reset
if st.sidebar.button("🔄 Switch User Type"):
    st.session_state.user_type = None
    rerun()

# --- Dynamic Footer ---
st.markdown("---")
if st.session_state.user_type == "Veterinary Professional":
    st.markdown("""
    <div style="text-align: center; font-size: 14px; color: #262262;">
        🩺 Built for vets by Bova UK | For veterinary professionals only. This app is for clinical support and educational use. | <a href="https://bova.vet/bova-uk/" target="_blank" style="color: #9b26b6;">Visit Bova UK</a>
    </div>
    """, unsafe_allow_html=True)

elif st.session_state.user_type == "Pet Owner":
    st.markdown("""
    <div style="text-align: center; font-size: 14px; color: #262262;">
        🐾 If you have a query about availability or ordering of medication to treat FIP please email sam@bova.co.uk

Contact your territory manager direct for the quickest response. | <a href="https://bova.vet/pet-owners/" target="_blank" style="color: #9b26b6;">Learn more</a>
    </div>
    """, unsafe_allow_html=True)
