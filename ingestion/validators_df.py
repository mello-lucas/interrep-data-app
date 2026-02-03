import pandas as pd

# colunas finais esperadas
EXPECTED_COLUMNS = {
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
}

NUMERIC_COLUMNS = {
    "goals",
    "own_goals",
    "assists",
    "yellow_cards",
    "blue_cards",
    "red_cards",
    "saves",
}

def validate_columns(df: pd.DataFrame) -> list[str]:
    missing = EXPECTED_COLUMNS - set(df.columns)
    if missing:
        return [f"Colunas ausentes: {', '.join(sorted(missing))}"]
    return []


def validate_row_count(df: pd.DataFrame) -> list[str]:
    if df.shape[0] == 0:
        return ["Nenhum jogador encontrado após o parse"]
    return []

def validate_numeric_types(df: pd.DataFrame) -> list[str]:
    errors = []

    for col in NUMERIC_COLUMNS:
        if not pd.api.types.is_integer_dtype(df[col]):
            errors.append(f"Coluna {col} não é inteira")
        elif (df[col] < 0).any():
            errors.append(f"Valores negativos encontrados em {col}")

    return errors


def validate_date(df: pd.DataFrame) -> list[str]:
    if not pd.api.types.is_datetime64_any_dtype(df["date"]):
        return ["Coluna date não é datetime"]
    return []

def validate_teams(df: pd.DataFrame) -> list[str]:
    teams = df["team"].dropna().unique()
    if len(teams) != 2:
        return [f"Número inválido de times: {len(teams)}"]
    return []


def validate_players(df: pd.DataFrame) -> list[str]:
    errors = []

    if df["name"].isna().any():
        errors.append("Existem jogadores sem nome")

    if df["nickname"].isna().any():
        errors.append("Existem jogadores sem apelido")

    return errors

def run_df_validations(df: pd.DataFrame) -> dict[str, list[str]]:
    validators = {
        "Schema": [
            validate_columns,
            validate_row_count,
        ],
        "Tipos": [
            validate_numeric_types,
            validate_date,
        ],
        "Semântica": [
            validate_teams,
            validate_players,
        ],
    }

    results = {}

    for group, funcs in validators.items():
        errors = []
        for fn in funcs:
            errors.extend(fn(df))
        if errors:
            results[group] = errors

    return results
