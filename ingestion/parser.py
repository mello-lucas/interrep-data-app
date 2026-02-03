import pandas as pd
import uuid
from datetime import datetime, timezone

STAT_COLUMNS = [
    "name",
    "nickname",
    "number",
    "goals",
    "own_goals",
    "assists",
    "yellow_cards",
    "blue_cards",
    "red_cards",
    "saves",
]

NUMERIC_COLUMNS = [
    "goals",
    "own_goals",
    "assists",
    "yellow_cards",
    "blue_cards",
    "red_cards",
    "saves",
]

FINAL_COLUMNS = [
    "ingestion_id",
    "ingested_at",
    "date",
    "championship",
    "round",
    "team",
    "name",
    "nickname",
    "goals",
    "own_goals",
    "assists",
    "yellow_cards",
    "blue_cards",
    "red_cards",
    "saves",
]


def clean_team_stats(df_stats: pd.DataFrame) -> pd.DataFrame:
    df = df_stats.copy()
    df.columns = STAT_COLUMNS
    df = df.drop(columns=["number"])

    df[NUMERIC_COLUMNS] = (
        df[NUMERIC_COLUMNS]
        .apply(pd.to_numeric, errors="coerce")
        .fillna(0)
        .astype(int)
    )

    return df


def parse_excel(file) -> pd.DataFrame:
    df = pd.read_excel(file, sheet_name="plan", header=None)

    championship = df.iloc[0, 0]
    game_date = pd.to_datetime(df.iloc[0, 1], dayfirst=True)
    round_name = df.iloc[1, 0]

    home_team = df.iloc[2, 1]
    away_team = df.iloc[23, 1]

    home = clean_team_stats(df.iloc[3:23, 0:10].dropna(how="all"))
    home["team"] = home_team

    away = clean_team_stats(df.iloc[24:, 0:10].dropna(how="all"))
    away["team"] = away_team

    df_final = pd.concat([home, away])

    df_final = df_final.assign(
        ingestion_id=uuid.uuid4(),
        ingested_at=datetime.now(timezone.utc),
        championship=championship,
        date=game_date,
        round=round_name,
    )

    return df_final[FINAL_COLUMNS]
