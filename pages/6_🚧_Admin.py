import streamlit as st
from utils.secrets import get_secret
from ingestion.parser import parse_excel
from ingestion.loader import load_to_raw
from ingestion.validators_file import validate_excel_structure
from ingestion.validators_df import run_df_validations

st.title("Upload de Jogo")

password = st.text_input("Senha de administrador", type="password")

if not password:
    st.info("Informe a senha para habilitar o upload")
    st.stop()

if password != get_secret("ADMIN_PASSWORD"):
    st.error("Senha incorreta")
    st.stop()

st.success("Acesso autorizado")

if st.button("Atualizar dados"):
    with st.spinner("Atualizando dados..."):
        st.cache_data.clear()
    st.success("Dados atualizados com sucesso.")

file = st.file_uploader("Envie a planilha do jogo", type=["xlsx"])

if not file:
    st.stop()

# 1️⃣ validação de estrutura do Excel (antes do parse)
file_errors = validate_excel_structure(file)

if file_errors:
    st.error("Arquivo inválido")
    for err in file_errors:
        st.write(f"- {err}")
    st.stop()

# 2️⃣ parse seguro
df = parse_excel(file)

# 3️⃣ validação semântica do DataFrame
df_errors = run_df_validations(df)

if df_errors:
    st.error("Dados inválidos")
    for err in df_errors:
        st.write(f"- {err}")
    st.stop()

with st.expander("Pré-visualização"):
    st.dataframe(df)

if st.button("Confirmar upload"):
    with st.spinner("Processando e salvando dados..."):
        load_to_raw(df)
    st.success("Jogo ingerido com sucesso")
