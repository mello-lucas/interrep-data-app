from utils.secrets import get_secret
from sqlalchemy import create_engine
from sqlalchemy.dialects.postgresql import (
    UUID, TIMESTAMP, DATE, TEXT, INTEGER
)


def load_to_raw(df):
    engine = create_engine(get_secret("NEON_DATABASE_URL"))

    df.to_sql(
        "player_game_ingest",
        engine,
        schema="raw",
        if_exists="append",
        index=False,
        method="multi",
        chunksize=1000,
        dtype={
            "ingestion_id": UUID(as_uuid=True),
            "ingested_at": TIMESTAMP(timezone=True),
            "date": DATE(),
            "championship": TEXT(),
            "round": TEXT(),
            "team": TEXT(),
            "name": TEXT(),
            "nickname": TEXT(),
            "goals": INTEGER(),
            "own_goals": INTEGER(),
            "assists": INTEGER(),
            "yellow_cards": INTEGER(),
            "blue_cards": INTEGER(),
            "red_cards": INTEGER(),
            "saves": INTEGER(),
        },
    )
