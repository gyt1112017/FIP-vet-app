import streamlit as st

def apply_theme():
    st.markdown("""
    <style>
    .st-av {
    background-color: #9b26b6;
}

/* Remove unwanted red borders that override your custom theme */
.st-e0, .st-dz, .st-dy, .st-dx {
    border-color: #9b26b6 !important;  /* or use #d3d3d3 for neutral */
    border-width: 1px !important;
    border-style: solid !important;
    border-radius: 10px !important;
}

    .stButton > button {
        background-color: #9b26b6;
        color: white;
        border: none;
        border-radius: 25px;
        padding: 10px 20px;
        font-size: 16px;
        width: 100%;
        margin-bottom: 10px;
    }
    .stButton > button:hover {
        background-color: #7e1d99;
        color: white;
    }
    
    button.custom-contact-button {
    background-color: #9b26b6;
    color: white;
    border: none;
    border-radius: 25px;
    padding: 10px 20px;
    font-size: 16px;
    width: 100%;
    transition: 0.3s ease;
    margin-bottom: 10px;
}
button.custom-contact-button:hover {
    background-color: #7e1d99;
}

    </style>
""", unsafe_allow_html=True)
