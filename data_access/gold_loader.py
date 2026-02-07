import pandas as pd
import streamlit as st
from utils.secrets import get_secret
from sqlalchemy import create_engine, text

engine = create_engine(get_secret("NEON_DATABASE_URL"))

@st.cache_data(ttl=3600)
def load_match_scoreboard() -> pd.DataFrame:
    query = """
        SELECT *
        FROM dbt_gold.match_scoreboard
        ORDER BY date DESC, championship ASC, round ASC
    """
    return pd.read_sql(text(query), engine)
