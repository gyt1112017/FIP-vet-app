import streamlit as st

def apply_theme():
    st.markdown("""
    <style>
    .st-av {
    background-color: #9b26b6;
}

/* Hover/focus effect for the step buttons */
button[data-testid="stNumberInputStepUp"]:hover,
button[data-testid="stNumberInputStepDown"]:hover,
button[data-testid="stNumberInputStepUp"]:focus,
button[data-testid="stNumberInputStepDown"]:focus {
    background-color: #9b26b6 !important;
    color: white !important;
}

/* 🟣 When clicked/focused: change border to brand purple */
div[data-testid="stNumberInputContainer"]:focus-within {
    border: 1px solid #9b26b6 !important;
}



/* Remove unwanted red borders that override your custom theme */
.st-e0, .st-dz, .st-dy, .st-dx {
    border-color: #d3d3d3 !important;  /* or use  for neutral */
    border-width: 1px !important;
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
