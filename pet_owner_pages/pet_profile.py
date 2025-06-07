import streamlit as st
from supabase import create_client
import uuid
import datetime

# Rerun helper
rerun = st.rerun if hasattr(st, "rerun") else getattr(st, "experimental_rerun", None)
if rerun is None:
    raise RuntimeError("Streamlit rerun function is unavailable")

# Supabase client for CRUD
sb = create_client(
    st.secrets['supabase']['url'],
    st.secrets['supabase']['key'],
)
sb_admin = create_client(
    st.secrets['supabase']['url'],
    st.secrets['supabase']['service_role_key'],
)

# Main page
def show():
    st.title("🐾 My Pet Profiles")
    st.markdown("Manage your pet’s details and track FIP diagnosis.")

    # Auth guard: require pet_user
    if "pet_user" not in st.session_state:
        st.warning("⚠️ You must be logged in to view this page.")
        st.stop()

    user_id = st.session_state['pet_user'].id

    # Fetch existing profiles for this user
    profiles = (
        sb.table("pet_profiles")
          .select("*")
          .eq("user_id", user_id)
          .execute()
    )
    data = profiles.data if hasattr(profiles, 'data') else profiles

    # Edit mode
    editing = st.session_state.get("editing_pet")

    st.subheader("📋 Pet Details")
    # Pre-fill values if editing
    name_default   = editing['pet_name'] if editing else ""
    breed_default  = editing['breed'] if editing else ""
    age_default = editing['age'] if editing else 0.0
    country_opts   = ["UK","USA","Australia","Other"]
    country_default= editing['country'] if editing else country_opts[0]
    practice_default = editing['practice'] if editing else ""
    neuter_opts    = ["Male, Entire","Male, Neutered","Female, Entire","Female, Neutered"]
    neuter_default = editing['neuter_status'] if editing else neuter_opts[0]
    fip_opts       = ["Wet FIP","Dry FIP","Neurological FIP","Ocular FIP"]
    fip_default    = editing['fip_type'] if editing else fip_opts[0]

    pet_name       = st.text_input("Pet Name", value=name_default)
    breed          = st.text_input("Breed", value=breed_default)
    age = st.number_input("Age (years)", min_value=0.0, step=0.5, value=age_default)
    country        = st.selectbox("Country", country_opts, index=country_opts.index(country_default))
    practice       = st.text_input("Veterinary Practice Name", value=practice_default)
    neuter_status  = st.selectbox("Neuter Status", neuter_opts, index=neuter_opts.index(neuter_default))
    fip_type       = st.selectbox("FIP Type", fip_opts, index=fip_opts.index(fip_default))

    st.subheader("🖼️ Pet Photo (optional)")
    uploaded_photo = st.file_uploader("Upload a photo of your pet", type=["jpg","jpeg","png"])

    # Save/Update
    if st.button("💾 Save Profile"):
        pet_id = editing['pet_id'] if editing else str(uuid.uuid4())
        photo_url = None
        if uploaded_photo:
            # upload to storage
            bucket = sb.storage.from_('petphotos')
            filename = f"{pet_id}_{uploaded_photo.name}"
            bucket.upload(filename, uploaded_photo)
            photo_url = bucket.get_public_url(filename)
        elif editing:
            photo_url = editing.get('photo_url')

        record = {
            'user_id':       user_id,
            'pet_id':        pet_id,
            'pet_name':      pet_name,
            'breed':         breed,
            'age':           age,
            'country':       country,
            'practice':      practice,
            'neuter_status': neuter_status,
            'fip_type':      fip_type,
            'photo_url':     photo_url,
            'updated_at':    datetime.datetime.utcnow().isoformat()
        }
        if editing:
            sb_admin.table("pet_profiles").update(record).eq('pet_id', pet_id).execute()
            st.success("✅ Profile updated")
            st.session_state['editing_pet'] = None
        else:
            record['created_at'] = datetime.datetime.utcnow().isoformat()
            sb_admin.table("pet_profiles").insert(record).execute()
            st.success("✅ Profile created")
        rerun()

    st.markdown("---")
    st.subheader("🔍 My Saved Profiles")
    if not data:
        st.info("No profiles yet. Use the form above to add a pet.")
        return

    # List profiles
    for pet in data:
        st.markdown(f"**{pet['pet_name']}** ({pet['breed']}, {pet['age']}y)")
        st.markdown(f"FIP Type: {pet['fip_type']}")
        if pet.get('photo_url'):
            st.image(pet['photo_url'], width=200)
        cols = st.columns([1,1])
        if cols[0].button("✏️ Edit", key=f"edit_{pet['pet_id']}"):
            st.session_state['editing_pet'] = pet
            rerun()
        if cols[1].button("🗑️ Delete", key=f"del_{pet['pet_id']}"):
            sb_admin.table("pet_profiles").delete().eq('pet_id', pet['pet_id']).execute()
            st.success("🗑️ Profile deleted")
            rerun()



