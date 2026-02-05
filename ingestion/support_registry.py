# %%
import pandas as pd
import os
import uuid
from datetime import datetime, timezone
from sqlalchemy import create_engine
from sqlalchemy.dialects.postgresql import (
    UUID, TIMESTAMP, TEXT, INTEGER
)

FILE = "../data/planilha_interrep_teste.xlsx"

EXPECTED_COLUMNS = ["Ano", "Campeonato", "Time", "Nome", "Apelido"]

FINAL_COLUMNS = [
    "ingestion_id",
    "ingested_at",
    "year",
    "championship",
    "team",
    "name",
    "nickname",
]


df = pd.read_excel(FILE, sheet_name="suport")
df = df[EXPECTED_COLUMNS]

df = df.dropna(how="all")

df = df.assign(
    ingestion_id=uuid.uuid4(),
    ingested_at=datetime.now(timezone.utc),
)

df = df.rename(columns={
    "Ano": "year",
    "Campeonato": "championship",
    "Time": "team",
    "Nome": "name",
    "Apelido": "nickname"
})

df = df[FINAL_COLUMNS]
df
# %%
engine = create_engine(os.getenv("NEON_DATABASE_URL"))

df.to_sql(
    "support_registry",
    engine,
    schema="raw",
    if_exists="append",
    index=False,
    method="multi",
    chunksize=1000,
    dtype={
        "ingestion_id": UUID(as_uuid=True),
        "ingested_at": TIMESTAMP(timezone=True),
        "year": INTEGER(),
        "championship": TEXT(),
        "team": TEXT(),
        "name": TEXT(),
        "nickname": TEXT(),
    },
)

# %%
