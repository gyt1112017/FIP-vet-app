import streamlit as st
def show():
    st.title("🎓 FIP Learning Hub")

    st.markdown("Discover our latest FIP CPD resources:")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div style="border:2px solid #9b26b6; border-radius:15px; padding:1rem; margin-bottom:1rem;">
            <h4 style="color:#9b26b6;">🎥 FIP On-demand Webinars</h4>
            <p>Get confident with diagnosing FIP in first opinion practice.</p>
            <a href="https://bova.vet/tag/feline-infectious-peritonitis/" target="_blank" style="color:#9b26b6; text-decoration:none; font-weight:bold;">
                🔗 Explore more
            </a>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style="border:2px solid #9b26b6; border-radius:15px; padding:1rem;">
            <h4 style="color:#9b26b6;">🎧 FIP Podcasts</h4>
            <p>Discussing treatment, owner communication, and real-world experiences.</p>
            <a href="https://yourpodcastlink.com" target="_blank" style="color:#9b26b6; text-decoration:none; font-weight:bold;">
                🎧 Listen Now
            </a>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style="border:2px solid #9b26b6; border-radius:15px; padding:1rem; margin-bottom:1rem;">
            <h4 style="color:#9b26b6;">📖 FIP Blogs </h4>
            <p>The treatment of feline infectious peritonitis (FIP) in the UK– an update FIP treatment protocols – what’s new?</p>
            <a href="https://bova.vet/2023/08/10/fip-an-update/" target="_blank" style="color:#9b26b6; text-decoration:none; font-weight:bold;">
                📚 Read Blog
            </a>
        </div>
        """, unsafe_allow_html=True)