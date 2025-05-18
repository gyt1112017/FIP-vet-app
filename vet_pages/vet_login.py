# vet_pages/vet_login.py
import streamlit as st
from supabase import create_client

# Initialize Supabase client from your secrets
sb = create_client(
    st.secrets["supabase"]["url"],
    st.secrets["supabase"]["key"],
)

def login():
    # ─── 0) Handle the magic-link callback ───
    params = st.query_params()
    token  = params.get("token", [None])[0]         # e.g. the TokenHash in your email link
    otp_type = params.get("type", ["magiclink"])[0] # should match 'magiclink'

    if token:
        # Exchange the token_hash for a session & user
        resp = sb.auth.verify_otp({
            "token_hash": token,   # note: verify_otp expects the hash
            "type":       otp_type
        })
        err  = getattr(resp, "error", None)
        user = getattr(resp, "user",  None)

        if err:
            st.error(f"🔐 Magic-link verification failed: {err}")
        else:
            # Success! Cache the user & rerun so the app unlocks
            st.session_state.vet_user = user
            st.success("✅ You’re now logged in!")
            st.experimental_rerun()

    # ─── 1) If already logged in, nothing else to do ───
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

        # This triggers Supabase to email a magic-link to the vet
        res = sb.auth.sign_in_with_otp({"email": email})
        err = getattr(res, "error", None) or (res.get("error") if isinstance(res, dict) else None)

        if err:
            msg = err.get("message") if isinstance(err, dict) else err
            st.error(f"Error sending magic link: {msg}")
        else:
            st.success("📬 Magic link sent! Check your inbox.")
            st.stop()
