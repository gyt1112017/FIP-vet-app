# Page: Diagnosis Guide
import streamlit as st
# vet_dry_fip.py
import streamlit as st

def show():
    st.title("Dry (Non-Effusive) FIP Diagnostic Tool")
    st.markdown("Use this flow to interpret your clinical chemistry results.")

    st.markdown("### A/G ratio (albumin / globulin)")
    ag = st.radio("A/G ratio", ["\> 0.8", "0.4 – 0.8", "< 0.4"], index=1, label_visibility="collapsed")

    st.markdown("### Globulin (g/L)")
    glob = st.radio("Globulin", ["< 25", "25 – 45", " \> 46"], index=1, label_visibility="collapsed")

    st.markdown("### Bilirubin")
    bili = st.radio("Bilirubin", ["Normal", "Raised"], index=0, label_visibility="collapsed")

    st.markdown("### Haematocrit (HCT)")
    hct = st.radio("Haematocrit", [" \> 30%", "< 30%"], index=0, label_visibility="collapsed")

    st.markdown("### Anaemia type")
    anaemia = st.radio("Anaemia type", ["Regenerative", "Non-regenerative"], index=0, label_visibility="collapsed")

    st.markdown("### Lymphocytes")
    lyph = st.radio("Lymphocytes", ["Normal", "Lymphopenia"], index=0, label_visibility="collapsed")

    st.markdown("### Neutrophils")
    neut = st.radio("Neutrophils", ["Normal", "Neutrophilia"], index=0, label_visibility="collapsed")

    st.markdown("### FCoV antibody test")
    fcov = st.radio("FCoV antibody test", ["Negative", "Positive"], index=0, label_visibility="collapsed")

    # Determine likely outcome
    not_fip = (ag == "\> 0.8" or
               glob == "25 – 45" and
               bili == "Normal" and
               hct == "\> 30%" and
               anaemia == "Regenerative" and
               lyph == "Normal" and
               neut == "Normal" or
               fcov == "Negative")

    possible = (ag == "< 0.4"
                or glob == "\> 46"
                or bili == "Raised"
                or hct == "< 30%"
                or anaemia == "Non-regenerative"
                or lyph == "Lymphopenia"
                or neut == "Neutrophilia"
                or fcov == "Positive")

    # Display outcome
    st.markdown("---")
    if not_fip:
        st.success("✅ **NOT FIP** – Normal profile. Consider other causes.")
    elif possible and fcov == "Negative":
        st.warning("⚠️ **FIP UNLIKELY** – Antibody negative. Consider other causes.")
    elif possible and fcov == "Positive":
        st.warning("⚠️ **FIP POSSIBLE** – Further specialised testing recommended.")
        st.markdown("""
        ### 🧪 External Lab Specialised Tests:
        - **Alpha-1 Glycoprotein (AGP)**  
          - \> 1500 µg/mL → 🟥 **FIP CONFIRMED: Start PI (Polyprenyl Immunostimulant) immediately**
          - Normal → Not FIP

        - **FCoV RT-PCR** on:
          - Aqueous humour  
          - FNA of mesenteric lymph node (recommended)  
          - Biopsy (IHC or RT-PCR)

            - If positive → 🟥 **FIP CONFIRMED: Start PI (Polyprenyl Immunostimulant) immediately**
            - Negative → FIP is not excluded. Consider clinical signs and other differentials diagnoses. 
        """)
    else:
        st.info("ℹ️ **Inconclusive** – consider external lab specialised tests (AGP, FCoV RT-PCR, IHC) based on clinical suspicion.")


