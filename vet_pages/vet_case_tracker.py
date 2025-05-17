import streamlit as st
from supabase import create_client
from io import BytesIO
from fpdf import FPDF
def _sanitize(text):
    try:
        return text.encode('latin-1', 'ignore').decode('latin-1')
    except:
        return str(text)

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
    with st.expander("➕ Add new case", expanded=True):
        # Animal details
        patient_id = st.text_input("Patient ID", help="Unique identifier for this patient")
        patient_name = st.text_input("Patient Name")
        treatment_date = st.date_input("Treatment Date")
        weight_kg = st.number_input("Weight (kg)", min_value=0.0, step=0.1)
        diagnosis = st.text_area("Diagnosis")
        breed = st.text_input("Breed")
        age_years = st.number_input("Age (years)", min_value=0, step=1)
        age_months = st.number_input("Age (months)", min_value=0, max_value=11, step=1)
        sex = st.selectbox("Sex", ["Male", "Female"])
        neuter_status = st.selectbox("Neutered status", ["Neutered", "Intact"])

        # Clinical history
        history = st.text_area(
            "History & Presenting Complaint",
            help="Summarise duration, clinical signs, weight change, appetite, environment",
            placeholder="e.g., '2-week diarrhoea with haematochezia, weight loss, normal appetite'"
        )

        # Diagnostic summaries
        lab_results = st.text_area(
            "Lab Results",
            help="Hematology and biochemistry findings (e.g., A:G ratio, ALT/GGT, PCV)",
            placeholder="Hematology and biochemistry findings (e.g., A:G ratio, ALT/GGT, PCV)"
        )
        imaging_findings = st.text_area(
            "Imaging Findings",
            help="Ultrasound/radiography results (e.g., effusion, organomegaly)",
            placeholder="Ultrasound/radiography results (e.g., effusion, organomegaly)"
        )

        # Effusion/Fluid diagnostics
        fluid_summary = st.text_area(
            "Effusion/Fluid Analysis",
            help="Appearance, protein, cytology, Rivalta, RT-PCR results",
            placeholder="Appearance, protein, cytology, Rivalta, RT-PCR results"
        )

        # Treatment & Outcome
        treatment_plan = st.text_area(
            "Treatment Plan & Progress",
            help="Medications, dosage, response, follow-up labs",
            placeholder="Medications, dosage, response, follow-up labs"
        )
        owner_concerns = st.text_area(
            "Owner Concerns",
            help="Environmental or historical factors noted by owner",
            placeholder="Environmental or historical factors noted by owner"
        )

        # Buttons: Save to database or Save as PDF
        if st.button("Save case"):
                payload = {
                    "vet_id": st.session_state.vet_user.id,
                    "patient_id": patient_id,
                    "patient_name": patient_name,
                    "breed": breed,
                    "age_years": age_years,
                    "age_months": age_months,
                    "sex": sex,
                    "neuter_status": neuter_status,
                    "history": history,
                    "diagnosis": diagnosis,
                    "lab_results": lab_results,
                    "imaging_findings": imaging_findings,
                    "fluid_summary": fluid_summary,
                    "treatment_plan": treatment_plan,
                    "owner_concerns": owner_concerns,
                }
                try:
                    res = sb_admin.table("cases").insert(payload).execute()
                    if getattr(res, "status_code", 200) >= 400:
                        st.error(f"Error saving case: {res.status_code} - {res.status_text}")
                    else:
                        st.success("✅ Case added to database!")
                except Exception as e:
                    st.error(f"Error saving case: {e}")

    # —–– List Existing Cases –––—
    cases = (
        sb_admin.table("cases")
        .select("*")
        .eq("vet_id", st.session_state.vet_user.id)
        .order("created_at", desc=True)
        .execute()
        .data
    )

    st.markdown("---")
    if cases:
        # Hide internal columns
        display_cases = [
            {k: v for k, v in c.items() if k not in ["id", "vet_id"]}
            for c in cases
        ]
        st.dataframe(display_cases, use_container_width=True)

        # Select one case to export
        case_map = {c.get("patient_id") or c["id"]: c for c in cases}
        selection = st.selectbox(
            "Select case to export:",
            options=list(case_map.keys()),
            format_func=lambda x: f"{x} | {case_map[x]['patient_name']}"
        )
        if st.button("Export to PDF Report"):
            record = case_map[selection]
            # Build PDF using selected record, not form variables
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Helvetica", size=16)
            pdf.cell(0, 10, f"FIP Case Report | {_sanitize(record.get('patient_name', ''))}", ln=True)
            pdf.ln(4)
            pdf.set_font("Helvetica", size=12)
            pdf.cell(0, 8, f"Patient ID: {_sanitize(record.get('patient_id', ''))}", ln=True)
            pdf.cell(0, 8, f"Treatment Date: {_sanitize(record.get('treatment_date', ''))}", ln=True)
            pdf.cell(0, 8, f"Weight (kg): {_sanitize(str(record.get('weight_kg', '')))}", ln=True)
            pdf.cell(0, 8, f"Breed: {_sanitize(record.get('breed', ''))}", ln=True)
            pdf.cell(0, 8, f"Age: {record.get('age_years', 0)}y {record.get('age_months', 0)}m", ln=True)
            pdf.cell(0, 8,
                     f"Sex&Neutered status: {_sanitize(record.get('sex', ''))}, {_sanitize(record.get('neuter_status', ''))}",
                     ln=True)
            pdf.ln(4)
            pdf.multi_cell(0, 8, f"History & Complaint: {_sanitize(record.get('history', ''))}")
            pdf.ln(4)
            pdf.multi_cell(0, 8, f"Diagnosis: {_sanitize(record.get('diagnosis', ''))}")
            pdf.ln(4)
            pdf.multi_cell(0, 8, f"Lab Results: {_sanitize(record.get('lab_results', ''))}")
            pdf.ln(4)
            pdf.multi_cell(0, 8, f"Imaging Findings: {_sanitize(record.get('imaging_findings', ''))}")
            pdf.ln(4)
            pdf.multi_cell(0, 8, f"Fluid Analysis: {_sanitize(record.get('fluid_summary', ''))}")
            pdf.ln(4)
            pdf.multi_cell(0, 8, f"Treatment Plan: {_sanitize(record.get('treatment_plan', ''))}")
            pdf.ln(4)
            pdf.multi_cell(0, 8, f"Owner Concerns: {_sanitize(record.get('owner_concerns', ''))}")
            pdf.ln(6)
            pdf.set_font("Helvetica", size=10)
            pdf.cell(0, 8, f"Created at: {record.get('created_at', '')}", ln=True)

            bio = BytesIO()
            bio.write(pdf.output(dest="S").encode("latin1", "ignore"))
            bio.seek(0)
            st.download_button(
                "Download Case PDF",
                data=bio,
                file_name=f"{_sanitize(record.get('patient_id', ''))}_{_sanitize(record.get('patient_name', ''))}_report.pdf",
                mime="application/pdf"
            )

