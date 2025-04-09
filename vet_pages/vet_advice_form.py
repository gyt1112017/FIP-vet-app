import streamlit as st

def show():
    st.title("📋 Request FIP Treatment Advice")

    st.markdown("If you are a vet and need to speak to a specialist then fill out this form to go to our  RCVS Recognised Feline Specialist, please indicate if your query is urgent")

    st.markdown("""
    <iframe src="https://share-eu1.hsforms.com/2-vQDDglDQEiXj5qyyc9Vzwg2km5"
            width="100%" height="800" style="border: none;">
    </iframe>
    """, unsafe_allow_html=True)
