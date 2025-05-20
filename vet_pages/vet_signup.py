# vet_pages/vet_register.py
import streamlit as st
from supabase import create_client
rerun = st.rerun if hasattr(st, "rerun") else st.experimental_rerun
# Admin client (service role) to query existing users
tmp = create_client(
    st.secrets['supabase']['url'],
    st.secrets['supabase']['service_role_key'],
)
sb_admin = tmp
sb = create_client(
    st.secrets['supabase']['url'],
    st.secrets['supabase']['key'],
)

def register():
    st.header("Vet Registration")
    st.write("Enter your work email to register. If your email is already in our system, you'll need to switch to login.")

    email = st.text_input("Email", placeholder="you@clinic.com", key="register_email")
    if st.button("Send Registration Code", key="send_register_otp"):
        if not email:
            st.error("Please enter your email address.")
            return

        # 1) Check if user already exists in Auth.Users table
        try:
            admin_resp = sb_admin.auth.admin.list_users()
            # list_users may return a list or dict
            if isinstance(admin_resp, dict):
                # new supabase-py: { "users": [...] }
                users = admin_resp.get('users') or admin_resp.get('data') or []
            elif isinstance(admin_resp, list):
                # older supabase-py might return list directly
                users = admin_resp
            else:
                users = []
            existing_user = any(
                (u.email if hasattr(u, 'email') else u.get('email')) == email
                for u in users if u
            )

        except Exception as e:
            st.error(f"Error checking existing users: {e}")
            return

        if existing_user:
            st.info("It looks like you already have an account. Please switch to **Login** in the sidebar.")
            return

        # 2) New user: send OTP to register (auto-create)
        try:
            res = sb.auth.sign_in_with_otp({"email": email})
        except Exception as e:
            st.error(f"Error sending registration code: {e}")
            return

        err = getattr(res, 'error', None) or (res.get('error') if isinstance(res, dict) else None)
        if err:
            msg = err.get('message') if isinstance(err, dict) else err
            st.error(f"Failed to send registration code: {msg}")
        else:
            st.success("Registration code sent! Check your email to complete registration.")
            rerun()



