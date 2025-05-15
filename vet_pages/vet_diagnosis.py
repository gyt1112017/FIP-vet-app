import streamlit as st

# --- Dry FIP Diagnostic ---
def show_dry():
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

    # Determine dry FIP outcome
    not_fip = (ag == "\> 0.8" or
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
        st.success("**NOT FIP** – Normal profile. Consider other causes.")
    elif possible and fcov == "Negative":
        st.warning("**FIP UNLIKELY** – Antibody negative. Consider other causes.")
    elif possible and fcov == "Positive":
        st.warning("**FIP POSSIBLE** – Further specialised testing recommended.")
        st.markdown("""
        ### External Lab Specialised Tests:
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
        st.info("**Inconclusive** – consider external lab specialised tests (AGP, FCoV RT-PCR, IHC) based on clinical suspicion.")

# --- Wet FIP Diagnostic ---
def show_wet():
    st.title("Wet (Effusive) FIP Diagnostic Tool")
    st.markdown("Use this flow to interpret your effusion fluid analysis results.")

    st.markdown("### Appearance of effusion")
    appearance = st.radio(
        "Appearance of effusion", [
            "Pus / blood / urine (smelly) / odiferous (smelly)",
            "Straw coloured / clear/ no odiferous (no smell)/ chylous (milky-like)",
        ], index=1, label_visibility="collapsed", key="wet_appearance"
    )

    st.markdown("### Protein content (g/L)")
    protein = st.selectbox(
        "Protein content", ["< 10", "10 – 35", "> 35"], index=1, label_visibility="collapsed", key="wet_protein"
    )

    st.markdown("### Albumin:Globulin ratio (a/g)")
    ag_ratio = st.selectbox(
        "Albumin:Globulin ratio", ["> 0.8", "< 0.8"], index=1, label_visibility="collapsed", key="wet_ag_ratio"
    )

    st.markdown("### Cytology")
    cytology = st.selectbox(
        "Cytology", [
            "Bacteria/malignant cells/mostly lymphocytes",
            "Neutrophils and macrophages"
        ], index=1, label_visibility="collapsed", key="wet_cytology"
    )

    st.markdown("### Rivalta test")
    rivalta = st.radio(
        "Rivalta test", ["Negative (NPV 93%)", "Positive (PPV 58%)"], index=0, label_visibility="collapsed", key="wet_rivalta"
    )

    st.markdown("### FCoV antibody test (blood)")
    fcov_eff = st.radio(
        "FCoV antibody test (blood)", ["Negative", "Positive"], index=0, label_visibility="collapsed", key="wet_fcov_eff"
    )

    # In-house decision logic
    not_fip_inhouse = (
            appearance == "Pus / blood / urine (smelly)" or
            protein == "< 10" or
            ag_ratio == "> 0.8" or
            cytology == "Bacteria/malignant cells/mostly lymphocytes"
    )
    unlikely_inhouse = (rivalta == "Negative (NPV 93%)" or fcov_eff == "Negative")
    possible_inhouse = not (not_fip_inhouse or unlikely_inhouse)
    st.markdown("---")
    if not_fip_inhouse:
        st.success("**NOT FIP** – Look for other causes.")
    elif unlikely_inhouse:
        st.warning("**FIP UNLIKELY** – But possible, consider other diagnoses.")
    else:
        st.warning("**FIP POSSIBLE** - \n**Next step:** send effusion for FCoV RT-PCR or AGP.")
    # Only if FIP unlikely or possible, offer RT-PCR
    if not not_fip_inhouse and (unlikely_inhouse or possible_inhouse):
        st.markdown("---")
        st.markdown("### External Lab: FCoV RT-PCR (on effusion)")
        rtpcr = st.radio(
            "RT-PCR result:", ["Negative", "Positive"], index=0, key="wet_rtpcr"
        )
        if rtpcr == "Negative":
            st.info("**Negative RT-PCR** – FIP is not excluded. Please consult differentials.")
        else:
            st.success("**FIP CONFIRMED** – Discuss treatment options")

# --- Neurological FIP Diagnostic ---
def show_neuro():
    st.title("Neurological FIP Diagnostic Tool")
    st.markdown("Use CSF analysis and follow-up sampling to assess neurological FIP.")

    st.markdown("### CSF sample: FCoV RT-PCR or immunostaining for FCoV antigen")
    initial = st.radio("Initial CSF result:", ["Either Positive", "Negative"], index=1, key="neuro_initial")

    if initial == "Either Positive":
        st.success("**FIP very likely**")
        st.markdown("**Next:** Consider a treatment trial with antiviral therapy (e.g., GS-441524).")
    else:
        st.warning("**FIP less likely**")
        st.markdown("If still suspicious, monitor non-neurological changes and sample other sites.")

        st.markdown("---")
        st.markdown("### Follow-up sampling (effusion RT-PCR / immunostaining)")
        follow = st.radio(
            "Follow-up result:",
            ["Positive FCoV RT-PCR with high FCoV RNA loads &/or positive immunostaining for FCoV antigen with cytology consistent for FIP", "Negative"],
            index=1,
            key="neuro_followup"
        )
        if follow.startswith("Positive"):
            st.success("**FIP very likely**")
        else:
            st.info("**Not positive on follow-up** – consider histopathology if available.")
            st.markdown("---")
            st.markdown("### Histopathology & immunohistochemistry")
            histo = st.radio(
                "Histopath result:",
                ["Consistent + antigen positive", "Not consistent / negative"],
                index=1,
                key="neuro_histo"
            )
            if histo.startswith("Consistent"):
                st.success("**FIP confirmed**")
            else:
                st.info("**FIP very unlikely**")

# --- Ocular FIP Diagnostic ---
def show_ocular():
    st.title("Ocular FIP Diagnostic Tool")
    st.markdown("Use aqueous humour sampling to assess ocular FIP.")

    st.markdown("### Aqueous humour sample analysis FCoV RT-PCR &/or immunostaining for FCoV antigen")
    init = st.radio(
        "", ["Either Positive", "Negative"], index=1, key="ocular_initial"
    )
    if init == "Either Positive":
        st.success("**FIP very likely**")
        st.markdown("**Next:** Consider a treatment trial with antiviral therapy (e.g., GS-441524).")
    else:
        st.warning("**FIP less likely**")
        st.markdown("Monitor non-ocular signs and sample other sites if suspicion remains.")
        st.markdown("---")
        st.markdown("### Follow-up sampling (body cavity centesis, FNA, trucut or full biopsy)")
        follow = st.radio(
            "", ["Positive FCoV RT-PCR with high FCoV RNA loads &/or positive immunostaining for FCoV antigen with Cytology consistent for FIP", "Histopathology consistent with FIP & positive immunohistochemistry for FCoV antigen","Not Consistent, Negative"],
            index=1, key="ocular_follow"
        )
        if follow.startswith("Positive"):
            st.success("**FIP very likely**")
        elif follow.startswith("Histopathology"):
            st.success("**FIP confirmed**")
        else:
            st.success("**FIP very unlikely**")

# --- Main show() ---
def show():
    st.header("FIP Diagnostics")
    choice = st.radio("Select FIP type:", ["Dry (Non-Effusive)", "Wet (Effusive)", "Neurological", "Ocular"], index=0, key="fip_type_selector")
    if choice == "Dry (Non-Effusive)":
        show_dry()
    elif choice == "Wet (Effusive)":
        show_wet()
    elif choice == "Neurological":
        show_neuro()
    else:
        show_ocular()
