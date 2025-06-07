import streamlit as st
from supabase import create_client

# Initialize Supabase client
sb = create_client(
    st.secrets['supabase']['url'],
    st.secrets['supabase']['key'],
)

# Rerun helper
rerun = st.rerun if hasattr(st, "rerun") else getattr(st, "experimental_rerun", None)
if rerun is None:
    raise RuntimeError("Streamlit rerun function is unavailable")

# Login function

def login():
    # If already logged in, do nothing - let app.py handle redirect
    if 'pet_user' in st.session_state:
        return

    st.header('🔑 Pet Owner Login via Email OTP')
    st.write('Enter your email, receive a 6-digit code, then verify to sign in.')

    # Email input
    email = st.text_input('Email', placeholder='you@petowner.com', key='po_login_email')

    # Send OTP
    if st.button('Send OTP Code', key='po_send_otp'):
        if not email:
            st.error('⚠️ Please enter your email address.')
        else:
            try:
                res = sb.auth.sign_in_with_otp({'email': email})
            except Exception as e:
                st.error(f'Error sending OTP: {e}')
            else:
                err = getattr(res, 'error', None) or (res.get('error') if isinstance(res, dict) else None)
                if err:
                    st.error(f'Failed to send OTP: {err.get("message", err)}')
                else:
                    st.success('✅ OTP sent! Check your email inbox.')
                    st.session_state['po_otp_requested'] = True

    # Verify OTP
    if st.session_state.get('po_otp_requested'):
        code = st.text_input('Enter OTP Code', placeholder='123456', key='po_otp_code')
        if st.button('Verify Code', key='po_verify_otp'):
            if not code:
                st.error('⚠️ Please enter the OTP code you received.')
            else:
                try:
                    resp = sb.auth.verify_otp({'email': email, 'token': code, 'type': 'email'})
                except Exception as e:
                    st.error(f'Error verifying OTP: {e}')
                    return

                err = getattr(resp, 'error', None) or (resp.get('error') if isinstance(resp, dict) else None)
                user = getattr(resp, 'user', None)
                if err or not user:
                    st.error(f"OTP verification failed: {err.get('message', err) if isinstance(err, dict) else err or 'Invalid code.'}")
                else:
                    # Successful login: set pet_user and a redirect flag
                    st.session_state['pet_user'] = user
                    st.session_state['redirect_to_profile'] = True
                    st.success('🎉 You’re now logged in!')
                    rerun()
