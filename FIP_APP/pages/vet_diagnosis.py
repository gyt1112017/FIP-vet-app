# Page: Diagnosis Guide
import streamlit as st
def show():
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