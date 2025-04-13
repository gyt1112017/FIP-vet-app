import streamlit as st
from supabase import create_client, Client
import uuid
import datetime
import os
# Supabase setup (replace with your actual keys)

SUPABASE_URL = "https://gljmgptmawpjpwntqtdm.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imdsam1ncHRtYXdwanB3bnRxdGRtIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDQ1NjUxNjAsImV4cCI6MjA2MDE0MTE2MH0.tL4Y8XXM2KnLKU0v91DsCy2n0-HdqcmBFi4s5HIznqI"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def show():
    st.title("🐾 Pet Profile Management")
    st.markdown("Manage your pet’s details and track FIP diagnosis.")

    st.subheader("📋 Pet Details")

    # Get logged-in user ID (assuming you're using Supabase Auth)
    user_id = None
    if 'user' in st.session_state:
        user_id = st.session_state.user.id
    else:
        st.warning("⚠️ You must be logged in to save your pet profile.")
        return

    pet_name = st.text_input("Pet Name")
    breed = st.text_input("Breed")
    age = st.number_input("Age (years)", min_value=0.0, step=0.5)
    country = st.selectbox("Country", ["UK", "USA", "Australia", "Other"])
    practice = st.text_input("Veterinary Practice Name")
    neuter_status = st.selectbox("Neuter Status", [
        "Male, Entire", "Male, Neutered",
        "Female, Entire", "Female, Neutered"])

    st.subheader("🧪 FIP Diagnosis Tracking")
    fip_type = st.radio("FIP Type", ["🟡 Wet FIP", "🔴 Dry FIP"])

    if st.button("💾 Save Profile"):
        if 'user' not in st.session_state:
            st.error("🚫 Please log in before saving a profile.")
            st.session_state.user_type = "Pet Owner"
            st.session_state.redirect_to_login = True
            st.experimental_rerun()
            return

        user_id = st.session_state.user.id
        pet_id = str(uuid.uuid4())

        data = {
            "pet_id": pet_id,
            "user_id": user_id,
            "email": st.session_state.user.email,
            "pet_name": pet_name,
            "breed": breed,
            "age": age,
            "country": country,
            "practice": practice,
            "neuter_status": neuter_status,
            "fip_type": fip_type,
            "created_at": datetime.datetime.utcnow().isoformat()
        }
        access_token = st.session_state.get("access_token")
        supabase.postgrest.auth(access_token)
        res = supabase.table("pet_profiles").insert(data).execute()

        if res.data:
            st.success("✅ Pet profile saved successfully!")
        else:
            st.error("❌ Failed to save profile. Please try again.")

    # Retrieve saved profiles by user_id
    if 'user' in st.session_state:
        user_id = st.session_state.user.id
        st.subheader("🔍 Retrieve Saved Profiles")

        if st.button("🔄 Load My Pet Profiles"):
            result = supabase.table("pet_profiles").select("*").eq("user_id", user_id).execute()

            if result.data:
                for pet in result.data:
                    st.markdown(f"**🐶 {pet['pet_name']}** - {pet['breed']} ({pet['age']} yrs)")
                    st.markdown(f"FIP Type: {pet['fip_type']}")
                    st.markdown(f"Practice: {pet['practice']}, Country: {pet['country']}")
                    st.markdown("---")
            else:
                st.info("No profiles found for your account.")


