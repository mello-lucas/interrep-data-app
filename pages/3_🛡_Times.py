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

st.title("🛡 Times")

df = load_player_summary()

col1, col2, col3 = st.columns(3)

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

with col3:
    selected_team = st.selectbox(
        "Time",
        options=sorted(df[(df["championship"] == selected_championship)]["team"].unique()),
        index=None,
        placeholder="Selecione o time"
    )

if not all([selected_year, selected_championship, selected_team]):
    st.info("Selecione ano, campeonato e time para visualizar as estatísticas.")
    st.stop()

st.divider()

df_filtered = df[
    (df["year"] == selected_year) &
    (df["championship"] == selected_championship) &
    (df["team"] == selected_team)
]

total_games = df_filtered["games_qty"].max()
total_goals = df_filtered["goals"].sum()
total_assists = df_filtered["assists"].sum()
total_cards = (
    df_filtered["yellow_cards"].sum()
    + df_filtered["blue_cards"].sum()
    + df_filtered["red_cards"].sum()
)
df_filtered["goal_rate"] = (
    df_filtered["games_with_goal"] / total_games
)
avg_goals_per_player = df_filtered["goals"].mean()

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    label="Jogos",
    value=total_games,
    help="Total de partidas disputadas pelo time no período selecionado"
)

col2.metric("Gols", total_goals)
col3.metric("Assistências", total_assists)
col4.metric("Cartões", total_cards)

st.divider()

st.subheader("🔥 Ranking de Gols")

df_plot = (
    df_filtered
    .sort_values("goals", ascending=True)
    .copy()
)

top_player = df_plot.iloc[-1]
others = df_plot.iloc[:-1]

fig = go.Figure()

# 🔹 Jogadores normais
fig.add_trace(
    go.Bar(
        x=others["goals"],
        y=others["nickname"],
        orientation="h",
        marker=dict(
            color="#fdf0d5"
        ),
        text=others["goals"],
        textposition="outside",
        hovertemplate=(
            "<b>%{y}</b><br>"
            "Gols: %{x}<br>"
            "Assistências: %{customdata[1]}<extra></extra>"
        ),
        customdata=others[["games_qty", "assists"]]
    )
)

# 🔥 Artilheiro principal
fig.add_trace(
    go.Bar(
        x=[top_player["goals"]],
        y=[top_player["nickname"]],
        orientation="h",
        marker=dict(
            color="#c1121f"
        ),
        text=[f"{top_player['goals']}"],
        textposition="outside",
        hovertemplate=(
            "🔥 <b>%{y}</b><br>"
            "Gols: %{x}<br>"
            "Assistências: %{customdata[1]}<extra></extra>"
        ),
        customdata=[[top_player["games_qty"], top_player["assists"]]]
    )
)

fig.update_layout(
    height=520,
    barmode="overlay",
    xaxis_title="Gols",
    yaxis_title="",
    margin=dict(l=20, r=20, t=40, b=20),
    showlegend=False
)

st.plotly_chart(fig, width="stretch")

st.divider()

st.subheader("📊 Estatísticas dos Jogadores")
DISPLAY_COLS = [
    "nickname",
    "goals",
    "assists",
    "goals_avg",
    "goal_rate",
    "yellow_cards",
    "blue_cards",
    "red_cards",
    "saves"
]

st.dataframe(
    df_filtered[DISPLAY_COLS]
    .sort_values("goals", ascending=False),
    column_config={
        "nickname": "Jogador",
        "goals": st.column_config.NumberColumn("Gols"),
        "assists": st.column_config.NumberColumn("Assistências"),
        "goals_avg": st.column_config.NumberColumn("Média de Gols", format="%.2f"),
        "goal_rate": st.column_config.ProgressColumn(
            "% Jogos com Gol",
            format="%.1f%%",
            min_value=0,
            max_value=1,
        ),
        "yellow_cards": st.column_config.NumberColumn("Amarelos"),
        "blue_cards": st.column_config.NumberColumn("Azuis"),
        "red_cards": st.column_config.NumberColumn("Vermelhos"),
        "saves": st.column_config.NumberColumn("Defesas"),
    },
    width="stretch",
    hide_index=True
)