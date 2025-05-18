# vet_pages/vet_login.py
import streamlit as st
from supabase import create_client

# Initialize Supabase client from your secrets
sb = create_client(
    st.secrets["supabase"]["url"],
    st.secrets["supabase"]["key"],
)

def login():
    # 0) Grab query params (token_hash & type)
    params      = st.query_params
    token_hash  = params.get("token_hash", [None])[0]
    otp_type    = params.get("type",       ["magiclink"])[0]

    if token_hash:
        # 1) Exchange hash for session & user
        resp = sb.auth.verify_otp({
            "token_hash": token_hash,
            "type":       otp_type
        })
        err  = getattr(resp, "error", None)
        user = getattr(resp, "user",  None)

        if err:
            st.error(f"🔐 Magic-link verification failed: {err}")
        else:
            st.session_state.vet_user = user
            st.success("✅ You’re now logged in via magic link!")
            st.experimental_rerun()

    # 2) If already logged in, stop here
    if "vet_user" in st.session_state:
        return

    # ─── 2) Otherwise show the “Send Magic Link” form ───
    st.header("🔐 Vet Login via Magic Link")
    st.write("Enter your work email and we’ll send you a login link.")
    email = st.text_input("Email", placeholder="you@clinic.com")

    if st.button("Send Magic Link"):
        if not email:
            st.error("Please enter an email address.")
            return

        # Include redirect_to so Supabase builds the correct link
        app_url = "https://fip-vet-app-bova.streamlit.app"
        res = sb.auth.sign_in_with_otp(
            {"email": email,
             "options": {
                 "email_redirect_to": app_url
             }
        )
        err = getattr(res, "error", None) or (res.get("error") if isinstance(res, dict) else None)
        if err:
            msg = err.get("message") if isinstance(err, dict) else err
            st.error(f"Error sending magic link: {msg}")
        else:
            st.success("📬 Magic link sent! Check your inbox.")
            st.stop()
