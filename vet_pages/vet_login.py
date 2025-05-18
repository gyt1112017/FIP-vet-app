# vet_pages/vet_login.py
import streamlit as st
from supabase import create_client

# Initialize Supabase
sb = create_client(
    st.secrets["supabase"]["url"],
    st.secrets["supabase"]["key"],
)

def login():
    st.header("🔐 Vet Login")
    email = st.text_input("Email")
    pw    = st.text_input("Password", type="password")

    if st.button("Log in"):
        # pick the right auth method for your client version
        auth_fn = (
            sb.auth.sign_in_with_password
            if hasattr(sb.auth, "sign_in_with_password")
            else sb.auth.sign_in
        )

        # perform the request in a try/except
        try:
            # v2 style: dict argument
            res = auth_fn({"email": email, "password": pw})
        except Exception as e:
            st.error(f"Authentication request failed:\n{e}")
            return

        # supabase-py v2 returns an object with .user / .error
        user = getattr(res, "user", None)
        error = getattr(res, "error", None)

        # supabase-py v1 returns a dict
        if user is None and isinstance(res, dict):
            user = res.get("user")
            error = res.get("error")

        if user:
            st.session_state.vet_user = user
            st.success("✅ Logged in successfully!")
        else:
            err_msg = error["message"] if isinstance(error, dict) and "message" in error else error
            st.error(f"Login failed: {err_msg}")
