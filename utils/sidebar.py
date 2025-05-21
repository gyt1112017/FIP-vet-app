# utils/sidebar.py
import streamlit as st

def show_shared_sidebar(rerun_fn):
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Need help?")
    st.sidebar.markdown(
        """
        <a href="https://bova.vet/bova-uk/contact-us/" target="_blank">
          <button class="custom-contact-button">Contact Us</button>
        </a>
        """,
        unsafe_allow_html=True,
    )

    if st.sidebar.button("Switch User Type"):
        st.session_state.user_type = None
        rerun_fn()
