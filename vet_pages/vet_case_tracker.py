import streamlit as st
from supabase import create_client
from io import BytesIO
from fpdf import FPDF
import base64


# Helper to sanitize non-Latin1 chars
def _sanitize(text):
    try:
        return text.encode('latin-1', 'ignore').decode('latin-1')
    except:
        return str(text)

# Main Case Tracker page
def show():
    # Rerun helper
    rerun = st.rerun if hasattr(st, "rerun") else getattr(st, "experimental_rerun", None)
    if rerun is None:
        raise RuntimeError("No rerun function available on this Streamlit version")

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

    # —Add New Case —
    with st.expander("➕ Add new case", expanded=False):
        # wrap all your inputs in a form that clears on submit
        with st.form("add_case_form", clear_on_submit=True):
            patient_id = st.text_input("Patient ID", help="Unique identifier for this patient")
            patient_name = st.text_input("Patient Name", help="Name for this patient")
            breed = st.text_input("Breed", help="Breed")
            age_years = st.number_input("Age (years)", min_value=0, step=1, help="Age year range")
            age_months = st.number_input("Age (months)", min_value=0, max_value=11, step=1, help="Age month range")
            sex = st.selectbox("Sex", ["Male", "Female"], help="Gender")
            neuter_status = st.selectbox("Neutered status", ["Neutered", "Intact"], help="Neutered status")
            treatment_date = st.date_input("Treatment Date", help="Date of treatment")
            weight_kg = st.number_input("Weight (kg)", min_value=0.1, step=0.1, value=0.1, format="%.1f", key="new_weight",help="Weight (kg)")
            diagnosis = st.selectbox("Diagnosis", ["Dry FIP", "Wet FIP","Neurological FIP","Ocular FIP"], help="Diagnosis")
            case_summary = st.text_area('Case Summary', help='Brief summary of clinical signs and diagnostics', placeholder="Summarise duration, clinical signs, weight change, appetite, environment")

            if st.form_submit_button("Save case"):
                if weight_kg <= 0:
                    st.error("⚠️ Weight (kg) is required and must be greater than 0.")
                else:
                    payload = {
                         'vet_id':         st.session_state.vet_user.id,
                         'patient_id':     patient_id,
                         'patient_name':   patient_name,
                         'breed':          breed,
                         'age_years':      age_years,
                         'age_months':     age_months,
                         'sex':            sex,
                         'neuter_status':  neuter_status,
                         'treatment_date': treatment_date.isoformat(),
                         'weight_kg':      weight_kg,
                         'diagnosis':      diagnosis,
                         'case_summary':   case_summary,
                    }
                try:
                    res = sb_admin.table("cases").insert(payload).execute()
                    if getattr(res, "status_code", 200) >= 400:
                        st.error(f"Error saving case: {res.status_code} - {res.status_text}")
                    else:
                        st.success("Case added to database!")
                        rerun()
                except Exception as e:
                    st.error(f"Error saving case: {e}")

    # —–– List Existing Cases –––—
    cases = (
        sb_admin.table("cases")
        .select("*")
        .eq("vet_id", st.session_state.vet_user.id)
        .order("created_at", desc=True)
        .execute().data
    )

    st.markdown("---")
    if not cases:
        st.info("No cases found. Use the form above to add a case.")
        rerun()

    # Display fields without ids
    display = []
    for c in cases:
        display.append({
                'Patient ID': c.get('patient_id', ''),
                'Name': c.get('patient_name', ''),
                'Breed': c.get('breed', ''),
                'Age': f"{c.get('age_years', 0)}y {c.get('age_months', 0)}m",
                'Sex': c.get('sex', ''),
                'Neutered': c.get('neuter_status', ''),
                'Date': c.get('treatment_date', ''),
                'Weight kg': c.get('weight_kg', ''),
                'Diagnosis': c.get('diagnosis', ''),
                'Summary': c.get('case_summary', ''),
        })
    st.dataframe(display, use_container_width=True)

    # Select and export
    keys = [c.get('patient_id') or c.get('id') for c in cases]
    sel = st.selectbox('Select case', options=keys, format_func=lambda x: next(
        (f"{c['patient_id']} | {c['patient_name']}" for c in cases if (c.get('patient_id') == x or c.get('id') == x)),
        x))
    record = next(c for c in cases if (c.get('patient_id') == sel))

    # --- Edit/Delete ---
    with st.expander('Edit/Delete selected case', expanded=False):
        e_name = st.text_input('Patient Name', value=record.get('patient_name', ''))
        e_breed = st.text_input('Breed', value=record.get('breed', ''))
        e_years = st.number_input('Age (years)', min_value=0, step=1, value=record.get('age_years', 0))
        e_months = st.number_input('Age (months)', min_value=0, max_value=11, step=1, value=record.get('age_months', 0))
        e_sex = st.selectbox('Sex', ['Male', 'Female'], index=0 if record.get('sex') == 'Male' else 1)
        e_neuter = st.selectbox('Neutered status', ['Neutered', 'Intact'],
                                index=0 if record.get('neuter_status') == 'Neutered' else 1)
        e_date = st.date_input('Treatment Date', value=record.get('treatment_date'))
        e_weight = st.number_input('Weight (kg)', min_value=0.0, step=0.1, value=record.get('weight_kg', 0.0))
        # Safe default for diagnosis
        diag_options = ['Dry FIP', 'Wet FIP', 'Neurological FIP', 'Ocular FIP']
        default_idx = diag_options.index(record.get('diagnosis')) if record.get('diagnosis') in diag_options else 0
        e_diag = st.selectbox('Diagnosis', diag_options, index=default_idx)
        e_summary = st.text_area('Case Summary', value=record.get('case_summary', ''))

        col1, col2 = st.columns(2)
        with col1:
            if st.button('Update case'):
                upd = {
                    'patient_name': e_name,
                    'breed': e_breed,
                    'age_years': e_years,
                    'age_months': e_months,
                    'sex': e_sex,
                    'neuter_status': e_neuter,
                    'treatment_date': e_date.isoformat(),
                    'weight_kg': e_weight,
                    'diagnosis': e_diag,
                    'case_summary': e_summary,
                }
                resp = sb_admin.table('cases').update(upd).eq('id', record['id']).execute()
                if getattr(resp, 'status_code', 200) >= 400:
                    st.error(f"Update failed: {resp.status_code} - {resp.status_text}")
                else:
                    st.success('Case updated')
                    rerun()
        with col2:
            if st.button('Delete case'):
                resp = sb_admin.table('cases').delete().eq('id', record['id']).execute()
                if getattr(resp, 'status_code', 200) >= 400:
                    st.error(f"Delete failed: {resp.status_code} - {resp.status_text}")
                else:
                    st.success('🗑️ Case deleted')
                    rerun()

    if st.button('Export to PDF'):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font('Helvetica', size=16)
        pdf.cell(0, 10, f"FIP Case Report - {_sanitize(record.get('patient_name', ''))}", ln=True)
        pdf.ln(4)
        pdf.set_font('Helvetica', size=12)
        pdf.multi_cell(0, 8, f"Patient ID: {_sanitize(record.get('patient_id', ''))}")
        pdf.multi_cell(0, 8, f"Name: {_sanitize(record.get('patient_name', ''))}")
        pdf.multi_cell(0, 8, f"Breed: {_sanitize(record.get('breed', ''))}")
        pdf.multi_cell(0, 8, f"Age: {record.get('age_years', 0)}y {record.get('age_months', 0)}m")
        pdf.multi_cell(0, 8,
                       f"Sex: {_sanitize(record.get('sex', ''))}, Neutered: {_sanitize(record.get('neuter_status', ''))}")
        pdf.multi_cell(0, 8, f"Date: {_sanitize(record.get('treatment_date', ''))}")
        pdf.multi_cell(0, 8, f"Diagnosis: {_sanitize(record.get('diagnosis', ''))}")
        pdf.multi_cell(0, 8, f"Weight(kg): {_sanitize(record.get('weight_kg', ''))}")
        pdf.multi_cell(0, 8, f"Summary: {_sanitize(record.get('case_summary', ''))}")

        pdf_bytes = pdf.output(dest="S").encode("latin1", "ignore")

        b64 = base64.b64encode(pdf_bytes).decode("utf-8")
        url = f"data:application/pdf;base64,{b64}"
        filename = f"{_sanitize(record['patient_id'])} | {_sanitize(record['patient_name'])}_report.pdf"

        # Single-line HTML (no leading spaces!)
        link_html = (
            f'<a href="{url}" '
            f'download="{filename}" '
            f'target="_blank" '
            f'style="font-size:1.1em; text-decoration:none;">'
            "📄 Download Case PDF (new tab)"
            "</a>"
        )

        st.markdown(link_html, unsafe_allow_html=True)
