import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from data_access.gold_loader import load_player_summary


st.set_page_config(
    page_title="Interrep — Data App",
    page_icon="⚽",
    layout="wide"
)

st.title("🏆 Rankings")

df = load_player_summary()

col1, col2 = st.columns(2)

with col1:
    selected_year = st.selectbox(
        "Ano",
        options=sorted(df["year"].astype(int).unique()),
        index=None,
        placeholder="Selecione o ano"
    )

with col2:
    selected_championship = st.selectbox(
        "Campeonato",
        options=sorted(df["championship"].unique()),
        index=None,
        placeholder="Selecione o campeonato"
    )

if not all([selected_year, selected_championship]):
    st.info("Selecione ano e campeonato para visualizar as estatísticas.")
    st.stop()

st.divider()

df_filtered = df[
    (df["year"] == selected_year) &
    (df["championship"] == selected_championship)
]

df_filtered["year"] = df_filtered["year"].astype(int)

for c in ["goals", "assists", "saves", "games_qty"]:
    if c in df_filtered.columns:
        df_filtered[c] = pd.to_numeric(df_filtered[c], errors="coerce").fillna(0).astype(int)

NAME_COL = "nickname"
TEAM_COL = "team"
GAMES_COL = "games_qty"

def make_top5(metric: str, title: str, emoji: str):
    cols = [NAME_COL, TEAM_COL, GAMES_COL, metric]

    top = (
        df_filtered
        .dropna(subset=[NAME_COL])
        .sort_values([metric, GAMES_COL, NAME_COL], ascending=[False, True, True], kind="mergesort")
        .head(5)
        .loc[:, cols]
        .rename(columns={
            NAME_COL: "Jogador",
            TEAM_COL: "Time",
            GAMES_COL: "Jogos",
            metric: "Total",
        })
    )

    st.subheader(f"{emoji} {title} (Top 5)")
    st.dataframe(top, use_container_width=True, hide_index=True)

colA, colB, colC = st.columns(3)

with colA:
    make_top5("goals", "Artilharia", "⚽")

with colB:
    make_top5("assists", "Assistências", "🎯")

with colC:
    make_top5("saves", "Defesa (Goleiros)", "🧤")

st.divider()