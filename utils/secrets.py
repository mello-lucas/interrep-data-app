import os
import streamlit as st

def get_secret(key: str):
    return st.secrets.get(key, os.getenv(key))