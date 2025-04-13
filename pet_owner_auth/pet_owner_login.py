import streamlit as st
from supabase import create_client

# Your Supabase keys
SUPABASE_URL = "https://gljmgptmawpjpwntqtdm.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imdsam1ncHRtYXdwanB3bnRxdGRtIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDQ1NjUxNjAsImV4cCI6MjA2MDE0MTE2MH0.tL4Y8XXM2KnLKU0v91DsCy2n0-HdqcmBFi4s5HIznqI"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
rerun = st.rerun if hasattr(st, "rerun") else st.experimental_rerun

def show():
    st.title("🐾 Pet Owner Login / Register")

    mode = st.radio("Select Mode", ["Login", "Register"])
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Submit"):
        if mode == "Register":
            result = supabase.auth.sign_up({
                "email": email,
                "password": password
            })
            if result.user:
                st.success("✅ Registered! Please verify your email.")
            else:
                st.error("Registration failed.")
        else:
            result = supabase.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            if result.user:
                st.session_state.user = result.user
                st.session_state.access_token = result.session.access_token
                st.session_state.user_type = "Pet Owner"

                # 🔁 Trigger redirect to Pet Profile
                st.session_state.redirect_to_profile = True

                st.success(f"Welcome {email}!")
                rerun()

            else:
                st.error("Login failed. Check your credentials.")
