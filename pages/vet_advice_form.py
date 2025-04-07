# Page: Request Advice
import streamlit as st
def show():
    st.title("📩 Request FIP Case Advice")

    with st.form("advice_form"):
        name = st.text_input("Your Name")
        practice = st.text_input("Practice Name")
        email = st.text_input("Email Address")
        notes = st.text_area("Case Summary / Questions")

        submitted = st.form_submit_button("Submit Advice Request")
        if submitted:
            st.success("✅ Thank you! A team member will be in touch shortly.")