import streamlit as st
from supabase import create_client
rerun = st.rerun if hasattr(st, "rerun") else st.experimental_rerun

# Initialize Supabase client
sb = create_client(
    st.secrets['supabase']['url'],
    st.secrets['supabase']['key'],
)

# Vet login via email OTP (one-time password)
def login():
    # If already logged in, nothing to do
    if 'vet_user' in st.session_state:
        return
    if 'otp_requested' not in st.session_state:
        st.session_state['otp_requested'] = False

    st.header('Vet Login')
    st.write('Enter your work email, receive a 6-digit code, then verify to sign in.')

    # Email input
    email = st.text_input('Email', placeholder='you@clinic.com', key='otp_email')

    # Step 1: Send OTP code (auto-creates user if new)
    if st.button('Send OTP Code'):
        if not email:
            st.error('Please enter your email address.')
        else:
            try:
                res = sb.auth.sign_in_with_otp({
                    'email': email,
                    'options': {
                        'should_create_user': False
                    }
                })
            except Exception as e:
                st.info("It looks like you haven't registered yet. Now please switch to **Register** in the sidebar to register")
                return
            err = getattr(res, 'error', None) or (res.get('error') if isinstance(res, dict) else None)
            if err:
                    msg = err.get('message') if isinstance(err, dict) else err
                    st.error(f'Failed to send OTP: {msg}')
            else:
                    st.success('OTP sent! Check your email inbox.')
                    st.session_state.otp_requested = True

    # Step 2: Verify OTP code
    if st.session_state.get('otp_requested'):
        code = st.text_input('Enter OTP Code', placeholder='123456', key='otp_code')
        if st.button('Verify Code'):
            if not code:
                st.error('Please enter the OTP code you received.')
            else:
                try:
                    resp = sb.auth.verify_otp({
                        'email': email,
                        'token': code,
                        'type': 'email'
                    })
                except Exception as e:
                    st.error(f'Error verifying OTP: {e}')
                    return

                err = getattr(resp, 'error', None) or (resp.get('error') if isinstance(resp, dict) else None)
                user = getattr(resp, 'user', None)
                if err or not user:
                    msg = err.get('message') if isinstance(err, dict) else err or 'Unknown error.'
                    st.error(f'OTP verification failed: {msg}')
                else:
                    st.session_state.vet_user = user
                    st.success('Logged in successfully!')
                    rerun()
