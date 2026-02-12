import pandas as pd
import numpy as np
import streamlit as st
from data_access.gold_loader import load_match_scoreboard

st.set_page_config(
    page_title="Interrep — Data App",
    page_icon="⚽",
    layout="wide"
)

st.title("🏟️ Jogos")

df = load_match_scoreboard()

with st.expander("Filtros", expanded=True):

    col1, col2, col3 = st.columns(3)

    with col1:
        championship = st.selectbox(
            "Campeonato",
            options=["Todos"] + sorted(df["championship"].dropna().unique().tolist())
        )

    with col2:
        round_ = st.selectbox(
            "Rodada",
            options=["Todas"] + sorted(df["round"].dropna().unique().tolist())
        )

    with col3:
        team = st.selectbox(
            "Time",
            options=["Todos"] + sorted(
                pd.unique(
                    df[["team", "team_opponent"]].values.ravel()
                )
            )
        )


df_filtered = df.copy()

if championship != "Todos":
    df_filtered = df_filtered[df_filtered["championship"] == championship]

if round_ != "Todas":
    df_filtered = df_filtered[df_filtered["round"] == round_]

if team != "Todos":
    df_filtered = df_filtered[
        (df_filtered["team"] == team) |
        (df_filtered["team_opponent"] == team)
    ]

df_view = (
    df_filtered
    .assign(
        match=lambda x: x["team"] + " x " + x["team_opponent"],
        score=lambda x: x["goals_scored"].astype(str)
        + " - "
        + x["goals_conceded"].astype(str),
        winner_team=lambda x: np.select(
            [
                x["goals_scored"] > x["goals_conceded"],
                x["goals_conceded"] > x["goals_scored"],
            ],
            [
                x["team"],
                x["team_opponent"],
            ],
            default="EMPATE",
        ),
        winner_badge=lambda x: np.select(
            [
                x["goals_scored"] > x["goals_conceded"],
                x["goals_conceded"] > x["goals_scored"],
            ],
            [
                "🏆 " + x["team"],
                "🏆 " + x["team_opponent"],
            ],
            default="🤝 Empate",
        ),
    )
    [[
        "date",
        "championship",
        "round",
        "match",
        "score",
        "winner_badge",
    ]]
    .sort_values("date", ascending=False)
)

st.dataframe(
    df_view,
    column_config={
        "date": "Data",
        "championship": "Campeonato",
        "round": "Rodada",
        "match": "Jogo",
        "score": "Placar",
        "winner_badge": "Resultado",
    },
    hide_index=True,
    width="stretch",
)

st.divider()

for _, row in df_view.iterrows():
    st.markdown(
        f"""
        ### {row['match']}
        **Placar:** {row['score']}  
        **Resultado:** {row['winner_badge']}  
        _{row['championship']} — Rodada {row['round']}_
        """
    )
    st.divider()
