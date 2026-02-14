import pandas as pd
import numpy as np
import streamlit as st

from data_access.gold_loader import load_player_summary, load_team_summary


st.set_page_config(
    page_title="Interrep — Data App",
    page_icon="⚽",
    layout="wide"
)

st.title("🏆 Rankings")

# -----------------------------
# Load
# -----------------------------
df_players = load_player_summary()
df_teams = load_team_summary()

# -----------------------------
# Global filters
# -----------------------------
col1, col2 = st.columns(2)

with col1:
    selected_year = st.selectbox(
        "Ano",
        options=sorted(df_players["year"].astype(int).unique()),
        index=None,
        placeholder="Selecione o ano"
    )

with col2:
    selected_championship = st.selectbox(
        "Campeonato",
        options=sorted(df_players["championship"].unique()),
        index=None,
        placeholder="Selecione o campeonato"
    )

if not all([selected_year, selected_championship]):
    st.info("Selecione ano e campeonato para visualizar as estatísticas.")
    st.stop()

st.divider()

# ============================================================
# 🧑‍💼 PLAYER RANKINGS
# ============================================================
st.markdown("## Ranking de Jogadores")

with st.container():

    df_p = df_players[
        (df_players["year"].astype(int) == int(selected_year)) &
        (df_players["championship"] == selected_championship)
    ].copy()

    # Tipagem
    for c in ["goals", "assists", "saves", "games_qty"]:
        if c in df_p.columns:
            df_p[c] = pd.to_numeric(df_p[c], errors="coerce").fillna(0).astype(int)

    NAME_COL = "nickname"
    TEAM_COL = "team"
    GAMES_COL = "games_qty"

    def make_top5(metric: str, title: str, emoji: str):
        cols = [NAME_COL, TEAM_COL, GAMES_COL, metric]
        cols = [c for c in cols if c in df_p.columns]

        top = (
            df_p
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
        if "goals" in df_p.columns:
            make_top5("goals", "Artilharia", "⚽")
        else:
            st.info("Coluna 'goals' não encontrada.")

    with colB:
        if "assists" in df_p.columns:
            make_top5("assists", "Assistências", "🎯")
        else:
            st.info("Coluna 'assists' não encontrada.")

    with colC:
        if "saves" in df_p.columns:
            make_top5("saves", "Defesa (Goleiros)", "🧤")
        else:
            st.info("Coluna 'saves' não encontrada.")

st.divider()

# ============================================================
# 🏟️ TEAM RANKINGS
# ============================================================
st.markdown("## 🏟️ Ranking de Times")

with st.popover("❓ Help — Siglas"):
    st.markdown("""
**Legenda da Tabela**

- **Pts** → Pontos (Vitória = 3, Empate = 1, Derrota = 0)
- **J** → Jogos
- **V** → Vitórias
- **E** → Empates
- **D** → Derrotas
- **GP** → Gols Pró (Gols Marcados)
- **GC** → Gols Contra (Gols Sofridos)
- **SG** → Saldo de Gols (GP − GC)
""")

with st.container():

    df_t = df_teams[
        (df_teams["year"].astype(int) == int(selected_year)) &
        (df_teams["championship"] == selected_championship)
    ].copy()

    # Tipagem numérica
    num_cols = ["goals_scored", "goals_conceded", "goals_diff", "wins", "losses", "draws", "games_qty", "points"]
    for c in num_cols:
        if c in df_t.columns:
            df_t[c] = pd.to_numeric(df_t[c], errors="coerce").fillna(0).astype(int)

    # Points (se não vier da Gold)
    if "points" not in df_t.columns:
        if "wins" in df_t.columns and "draws" in df_t.columns:
            df_t["points"] = (df_t["wins"] * 3 + df_t["draws"]).astype(int)
        else:
            df_t["points"] = 0

    # Ordenação estilo tabela
    sort_cols = [c for c in ["points", "goals_diff", "goals_scored", "games_qty", "team"] if c in df_t.columns]
    asc = []
    for c in sort_cols:
        if c in ["games_qty", "team"]:
            asc.append(True)
        else:
            asc.append(False)

    df_rank = (
        df_t.sort_values(sort_cols, ascending=asc, kind="mergesort")
            .reset_index(drop=True)
    )

    df_rank.insert(0, "pos", np.arange(1, len(df_rank) + 1))

    # Colunas exibidas
    show_cols = ["pos", "team", "points", "games_qty", "wins", "draws", "losses", "goals_scored", "goals_conceded", "goals_diff"]
    show_cols = [c for c in show_cols if c in df_rank.columns]

    st.dataframe(
        df_rank[show_cols].rename(columns={
            "pos": "#",
            "team": "Time",
            "points": "Pts",
            "games_qty": "J",
            "wins": "V",
            "draws": "E",
            "losses": "D",
            "goals_scored": "GP",
            "goals_conceded": "GC",
            "goals_diff": "SG",
        }),
        use_container_width=True,
        hide_index=True
    )

    # Top 5 cards (opcional, mas ajuda leitura)
    st.markdown("### Destaques (Top 5)")

    c1, c2, c3 = st.columns(3)

    with c1:
        if "goals_scored" in df_rank.columns:
            st.caption("Ataque (GP)")
            top = df_rank.sort_values(["goals_scored", "points"], ascending=[False, False]).head(5)
            st.dataframe(
                top[["team", "goals_scored", "games_qty"]].rename(columns={"team": "Time", "goals_scored": "GP", "games_qty": "J"}),
                use_container_width=True,
                hide_index=True
            )

    with c2:
        if "goals_conceded" in df_rank.columns:
            st.caption("Defesa (menos GC)")
            top = df_rank.sort_values(["goals_conceded", "points"], ascending=[True, False]).head(5)
            st.dataframe(
                top[["team", "goals_conceded", "games_qty"]].rename(columns={"team": "Time", "goals_conceded": "GC", "games_qty": "J"}),
                use_container_width=True,
                hide_index=True
            )

    with c3:
        if "goals_diff" in df_rank.columns:
            st.caption("Saldo (SG)")
            top = df_rank.sort_values(["goals_diff", "points"], ascending=[False, False]).head(5)
            st.dataframe(
                top[["team", "goals_diff", "games_qty"]].rename(columns={"team": "Time", "goals_diff": "SG", "games_qty": "J"}),
                use_container_width=True,
                hide_index=True
            )
