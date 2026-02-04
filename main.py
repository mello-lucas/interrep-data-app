# libs
import streamlit as st

st.set_page_config(
    page_title="Interrep — Data App",
    page_icon="⚽",
    layout="wide"
)

st.title("Interrep — Data App", text_alignment="center")

st.sidebar.image(
    "assets/logo.jpg",
    use_container_width=True
)

st.sidebar.markdown(
    "<hr style='border:1px solid #C9A227'>",
    unsafe_allow_html=True
)