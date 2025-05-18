# vet_pages/vet_login.py
import streamlit as st
from supabase import create_client

# Init Supabase client from your Streamlit Cloud secrets
sb = create_client(
    st.secrets["supabase"]["url"],
    st.secrets["supabase"]["key"],
)

def login():
    st.header("Vet Login via Magic Link")
    st.write("Enter your work email and we'll send you a secure login link.")
    email = st.text_input("Email", placeholder="you@clinic.com")

    if st.button("Send Magic Link"):
        if not email:
            st.error("Please enter your email address.")
            return

        try:
            # This triggers Supabase to email a magic-link to the vet
            res = sb.auth.sign_in_with_otp({
                'email': email,
                'options': {
                'should_create_user': False,
                'email_redirect_to': 'https://fip-vet-app-bova.streamlit.app/',
            },
            })

        except Exception as e:
            st.error(f"Failed to send magic link:\n{e}")
            return

        # supabase-py v2 returns an object with .error
        err = getattr(res, "error", None)
        # supabase-py v1 returns a dict
        if not err and isinstance(res, dict):
            err = res.get("error")

        if err:
            # Present whatever message Supabase returned
            msg = err.get("message") if isinstance(err, dict) else err
            st.error(f"Error sending magic link: {msg}")
        else:
            st.success(
                "Magic link sent! Check your inbox for an email from us."
            )
            st.stop()
