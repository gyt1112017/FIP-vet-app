import streamlit as st
from utils.styling import apply_theme
apply_theme()
from utils.sidebar import show_shared_sidebar
from vet_pages import vet_login, vet_signup, vet_diagnosis, vet_dose_calculator, vet_case_tracker, vet_learning, vet_cascade_guide
from pet_owner_pages import pet_profile

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
    choice = st.sidebar.selectbox("Vet Access", ["Register", "Login"], key="vet_auth_mode")
    # ───── Vet Auth ─────
    if choice == "Register":
        from vet_pages.vet_signup import register
        register()
        st.stop()
    else:
        from vet_pages.vet_login import login
        login()
        if "vet_user" not in st.session_state:
            st.stop()

    page = st.sidebar.radio("Vet Menu", [
        "Diagnosis Guide",
        "Dose Calculator",
        "Case Tracker",
        "FIP Learning Hub",
        "Vet Cascade Guide"
    ])

    if page == "Diagnosis Guide":
        vet_diagnosis.show()
    elif page == "Dose Calculator":
        vet_dose_calculator.show()
    elif page == "Case Tracker":
        vet_case_tracker.show()
    elif page == "FIP Learning Hub":
        vet_learning.show()
    elif page == "Vet Cascade Guide":
        vet_cascade_guide.show()

elif st.session_state.user_type == "Pet Owner":
    pet_owner_pages = {
        "Login / Register": "pet_owner_auth.pet_owner_login",
        "Pet Profile": "pet_owner_pages.pet_profile",
    }

    # Check for post-login redirect
    if st.session_state.get("redirect_to_profile", False):
        selected_page = "Pet Profile"
        st.session_state.redirect_to_profile = False  # Reset the flag
    elif st.session_state.get("redirect_to_login", False):
        selected_page = "Login / Register"
        st.session_state.redirect_to_login = False  # Reset login flag
    else:
        selected_page = st.sidebar.radio("Pet Owner Menu", list(pet_owner_pages.keys()))

    # Load the selected module dynamically
    module_path = pet_owner_pages[selected_page]
    module = __import__(module_path, fromlist=["show"])
    module.show()




# --- Sidebar ---

show_shared_sidebar(rerun)

# --- Dynamic Footer ---
st.markdown("---")
if st.session_state.user_type == "Veterinary Professional":
    st.markdown("""
    <div style="text-align: center; font-size: 14px; color: #262262;">
        Built for vets by Bova UK | For veterinary professionals only. This app is for clinical support and educational use. | <a href="https://bova.vet/bova-uk/" target="_blank" style="color: #9b26b6;">Visit Bova UK</a>
    </div>
    """, unsafe_allow_html=True)

elif st.session_state.user_type == "Pet Owner":
    st.markdown("""
    <div style="text-align: center; font-size: 14px; color: #262262;">
        <a>If you have a query about availability or ordering of medication to treat FIP please contact your vet</a>
    </div>
    """, unsafe_allow_html=True)
