import streamlit as st
from supabase import create_client

# Initialize Supabase
sb = create_client(
    st.secrets["supabase"]["url"],
    st.secrets["supabase"]["key"],
)

def login():
    # 0) Handle the magic‐link callback:
    params = st.experimental_get_query_params()
    token_hash = params.get("token_hash", [None])[0]
    otp_type   = params.get("type",      ["email"])[0]  # could be 'email', 'invite', etc.

    if token_hash:
        # Exchange the hash for a session & user
        resp = sb.auth.verify_otp({
            "token_hash": token_hash,
            "type":       otp_type
        })
        err = getattr(resp, "error", None)
        user = getattr(resp, "user",  None)
        if err:
            st.error(f"Magic-link verification failed: {err}")
        else:
            # Success! Cache the user in session_state
            st.session_state.vet_user = user
            st.success("✅ Logged in via magic link!")
            st.experimental_rerun()

    # 1) If we already have a logged-in user, stop here
    if "vet_user" in st.session_state:
        return

    # 2) Otherwise render the magic-link request form
    st.header("🔐 Vet Login via Magic Link")
    st.write("Enter your work email to receive a login link.")
    email = st.text_input("Email", placeholder="you@clinic.com")

    if st.button("Send Magic Link"):
        if not email:
            st.error("Please enter an email address.")
        else:
            res = sb.auth.sign_in_with_otp(
                {"email": email},
                # optionally:
                # {"email": email, "options": {"email_redirect_to": "https://your-app-url"}}
            )
            err = getattr(res, "error", None) or (res.get("error") if isinstance(res, dict) else None)
            if err:
                msg = err.get("message") if isinstance(err, dict) else err
                st.error(f"Error sending magic link: {msg}")
            else:
                st.success("📬 Magic link sent! Check your inbox.")
                st.stop()
