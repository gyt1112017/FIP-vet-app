import streamlit as st
from supabase import create_client
from io import BytesIO
from fpdf import FPDF

# Page configuration
def show():
    # Authentication guard
    if "vet_user" not in st.session_state:
        st.warning("Please log in as a veterinary professional to access the Case Tracker.")
        st.stop()

    # Public client (for reading via RLS / your anon policy)
    sb = create_client(st.secrets["supabase"]["url"],
                       st.secrets["supabase"]["key"])

    # Admin client (bypasses RLS) for inserts/updates/deletes
    sb_admin = create_client(st.secrets["supabase"]["url"],
                             st.secrets["supabase"]["service_role_key"])

    st.title("FIP Case Tracker")

    # —➕ Add New Case —
    with st.expander("Add new case", expanded=True):
        patient_id = st.text_input("Patient ID", help="Unique identifier for the patient")
        patient_name = st.text_input("Patient Name")
        treatment_date = st.date_input("Treatment Date")
        weight_kg = st.number_input("Weight (kg)", min_value=0.0, step=0.1, format="%.1f")
        diagnosis = st.text_area("Diagnosis")
        case_notes = st.text_area("Case Notes", help="Free-text observations and notes")
        if st.button("Save case"):
            payload = {
                "vet_id": st.session_state.vet_user.id,
                "patient_id": patient_id,
                "patient_name": patient_name,
                "treatment_date": treatment_date.isoformat(),
                "weight_kg": weight_kg,
                "diagnosis": diagnosis,
                "case_notes": case_notes,
            }
            try:
                res = sb_admin.table("cases").insert(payload).execute()
                # PostgrestResponse has status_code and status_text
                if getattr(res, "status_code", 200) >= 400:
                    st.error(f"Error saving case: {res.status_code} - {res.status_text}")
                else:
                    st.success("Case added!")
            except Exception as e:
                st.error(f"Error saving case: {e}")

    # —–– List Existing Cases –––—
    cases = (
        sb.table("cases")
        .select("*")
        .eq("vet_id", st.session_state.vet_user.id)
        .order("created_at", desc=True)
        .execute()
        .data
    )

