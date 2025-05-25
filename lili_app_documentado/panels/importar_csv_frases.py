import streamlit as st

def painel():
    import streamlit as st
    import pandas as pd

    def importar_csv_frases():
        st.header("📑 Importar Frases Clínicas (CSV)")

        arquivo_csv = st.file_uploader("Escolha um arquivo .csv com frases clínicas", type=["csv"])

        if arquivo_csv is not None:
            try:
                df = pd.read_csv(arquivo_csv)
                st.success("Arquivo CSV carregado com sucesso!")
                st.dataframe(df)
                st.session_state["frases_csv"] = df
            except Exception as e:
                st.error(f"Erro ao ler o arquivo CSV: {e}")