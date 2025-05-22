import streamlit as st
from datetime import datetime


def show():
    st.title("Cascade Justification Tool")

    st.markdown("### When is it appropriate to prescribe a **special formulation**?")
    st.write("Select any of the following reasons that apply to your current case:")

    # Interactive checkboxes
    reasons = {
        "individual": st.checkbox("The patient has individual characteristics (e.g. breed sensitivity, age)"),
        "chronic": st.checkbox("Condition persists despite licensed treatment (chronic infections)"),
        "unavailable": st.checkbox("Licensed product unavailable in time"),
        "owner": st.checkbox("Owner unable to administer licensed product (e.g. injection)")
    }

    selected = [key for key, val in reasons.items() if val]

    # Show interpretation
    st.markdown("---")
    if len(selected) >= 1:
        st.success("✅ Cascade justification is supported in this case.")
    else:
        st.info("ℹ️ Select at least one reason to determine cascade eligibility.")

    # Cascade context section
    st.markdown("---")
    st.markdown("### Prescribing Specials and the Cascade")
    st.markdown("""
    All Bova formulations are prescribed by veterinary surgeons, following the prescribing cascade. When there is no suitable licensed medication, then vets may use their clinical judgment to prescribe a special formulation, if appropriate.

    All our products are used in compliance with the:

    - [Veterinary Prescribing Cascade (VMD)](https://www.gov.uk/guidance/the-cascade-prescribing-unauthorised-medicines)
    - [Cascade: Extemporaneous Preparations – Specials (VMD)](https://www.gov.uk/guidance/the-cascade-prescribing-unauthorised-medicines#extemporaneous-preparations-specials)
    - [RCVS Code of Professional Conduct for Veterinary Surgeons](https://www.rcvs.org.uk/setting-standards/advice-and-guidance/code-of-professional-conduct-for-veterinary-surgeons/supporting-guidance/veterinary-medicines/)

    Section 4.15 of the RCVS Code of Professional Conduct states:
    ‘If there is no suitable authorised veterinary medicinal product in the UK for a condition in a particular species, a veterinary surgeon may, in particular, to avoid unacceptable suffering, treat the animal in accordance with the ‘Cascade’.
    """, unsafe_allow_html=True)

    # Embed cascade explainer video or link
    st.markdown("---")
    st.markdown("### Get confidence with Cascade:")
    st.markdown(
        """We know this can be a challenging area to navigate, especially if you are new to using Specials products, so we also have podcasts and a webinar on using the cascade. If you have any questions about the correct use of the cascade then please <a href='https://bova.vet/bova-uk/contact-us/' target='_blank'>get in touch.</a>""",
        unsafe_allow_html=True)
    st.video("https://www.youtube.com/watch?v=hggZPzVqqJE")
    st.video("https://youtu.be/vkRWI64hJDI")

    st.markdown("---")
    st.markdown("### Featured Cascade Podcasts")

    # Podcast 1 – Equine
    st.markdown("""
        #### Part 1: Equine — Dr. Mark Bowen
        _“Demystifying the cascade in equine cases with real-world examples. A must-listen for equine vets.”_

        <iframe src="https://www.buzzsprout.com/1871565/10556201-the-veterinary-prescribing-cascade-part-1-equine?client_source=small_player&iframe=true" 
                width="100%" height="220" frameborder="0" scrolling="no">
        </iframe>
        """, unsafe_allow_html=True)

    # Podcast 2 – Small Animal
    st.markdown("""
        #### Part 2: Small Animal — Dr. Mark Bowen
        _“Using the cascade in small animal cases, especially antimicrobial use, with post-Brexit context.”_

        <iframe src="https://www.buzzsprout.com/1871565/10557213-the-veterinary-prescribing-cascade-part-2-small-animal?client_source=small_player&iframe=true" 
                width="100%" height="220" frameborder="0" scrolling="no">
        </iframe>
        """, unsafe_allow_html=True)

