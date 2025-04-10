import streamlit as st
from datetime import datetime
import streamlit.components.v1 as components

def show():
    st.title("🧠 Cascade Justification Tool")

    st.markdown("### When is it appropriate to prescribe a **special formulation**?")
    st.write("Select any of the following reasons that apply to your current case:")

    # Interactive checkboxes
    reasons = {
        "individual": st.checkbox("🐾 The patient has individual characteristics (e.g. breed sensitivity, age)"),
        "chronic": st.checkbox("🧬 Condition persists despite licensed treatment (chronic infections)"),
        "unavailable": st.checkbox("🚫 Licensed product unavailable in time"),
        "owner": st.checkbox("👤 Owner unable to administer licensed product (e.g. injection)")
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
    st.markdown("### 📘 Prescribing Specials and the Cascade")
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
    st.markdown("### 🎥 Get confidence with Cascade:")
    st.markdown("""We know this can be a challenging area to navigate, especially if you are new to using Specials products, so we also have podcasts and a webinar on using the cascade. If you have any questions about the correct use of the cascade then please <a href='https://bova.vet/bova-uk/contact-us/' target='_blank'>get in touch.</a>""", unsafe_allow_html=True)
    st.video("https://www.youtube.com/watch?v=hggZPzVqqJE") 
    st.video("https://youtu.be/vkRWI64hJDI") 
    # Embed Buzzsprout podcast player using raw HTML + JS
buzzsprout_embed = """
<div id="buzzsprout-player-10556201"></div>
<script src="https://www.buzzsprout.com/1871565/episodes/10556201-the-veterinary-prescribing-cascade-part-1-equine.js?container_id=buzzsprout-player-10556201&player=small" 
type="text/javascript" charset="utf-8"></script>
"""

# Render it in the Streamlit app
components.html(buzzsprout_embed, height=200, scrolling=False)
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
            <div style="border:2px solid #9b26b6; border-radius:15px; padding:1rem; margin-bottom:1rem;">
                <h4 style="color:#9b26b6;">🎥 Cascade Webinars</h4>
                <p>Regarding the Cascade, how can you legally, as opposed to just medically, justify going straight to (extemporised) reformulation if you have not actually tried other options?’ Present by Danielle Gunn-Moore.</p>
                <a href="https://bova.vet/2018/07/13/regarding-the-cascade-how-can-you-legally-as-opposed-to-just-medically-justify-going-straight-to-extemporised-reformulation-if-you-have-not-actually-tried-other-options/" target="_blank" style="color:#9b26b6; text-decoration:none; font-weight:bold;">
                    🔗 Watch Now
                </a>
            </div>
            """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style="border:2px solid #9b26b6; border-radius:15px; padding:1rem; margin-bottom:1rem;">
            <h4 style="color:#9b26b6;">🎧 Cascade Podcasts </h4>
            <p>The veterinary prescribing cascade Small Animal and Equine By  Dr. Mark Bowen BVetMed MMedSci(MedEd) Ph.D. Cert VA Cert EM(IntMed) Dip ECVSMR Dip ACVIMLAIM PFHEA FRCVS.</p>
            <a href="https://bovaukpodcast.buzzsprout.com/1871565/episodes/10556201-the-veterinary-prescribing-cascade-part-1-equine" target="_blank" style="color:#9b26b6; text-decoration:none; font-weight:bold;">
                🎧 Listen Now
            </a>
        </div>
        """, unsafe_allow_html=True)
