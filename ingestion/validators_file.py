import pandas as pd

def validate_excel_structure(file) -> list[str]:
    errors = []

    try:
        xls = pd.ExcelFile(file)
    except Exception:
        return ["Arquivo não é um Excel válido"]

    if "plan" not in xls.sheet_names:
        errors.append("Aba 'plan' não encontrada")

    if errors:
        return errors

    df_raw = pd.read_excel(xls, sheet_name="plan", header=None)

    if df_raw.shape[0] < 25:
        errors.append("Layout incompatível: linhas insuficientes")

    if pd.isna(df_raw.iloc[0, 0]):
        errors.append("Campeonato não identificado (A1 vazia)")

    if pd.isna(df_raw.iloc[2, 1]) or pd.isna(df_raw.iloc[23, 1]):
        errors.append("Times não identificados")

    return errors
