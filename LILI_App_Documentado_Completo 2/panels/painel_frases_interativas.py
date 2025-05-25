
import streamlit as st
import pandas as pd
import difflib

def carregar_csv_frases():
    try:
        return pd.read_csv("frases.csv")
    except FileNotFoundError:
        st.warning("Arquivo frases.csv não encontrado.")
        return pd.DataFrame()

def inserir_automaticamente_em_laudo(descricao, conclusao):
    if "texto_laudo" not in st.session_state:
        st.session_state.texto_laudo = ""
    st.session_state.texto_laudo += f"\n{descricao}"
    if conclusao and conclusao.strip():
        st.session_state.texto_laudo += f"\nConclusão: {conclusao}"

def painel_frases_interativas():
    st.header("📌 Buscar e Inserir Frases no Laudo")

    df = carregar_csv_frases()
    if df.empty:
        return

    sistema_selecionado = st.selectbox("🔍 Filtrar por sistema", ["Todos"] + sorted(df["sistema"].dropna().unique().tolist()))
    termo_busca = st.text_input("🧠 Digite uma palavra-chave para buscar alterações:")

    resultados = df.copy()
    if sistema_selecionado != "Todos":
        resultados = resultados[resultados["sistema"] == sistema_selecionado]

    if len(termo_busca) >= 3:
        todas_alteracoes = resultados["nome_da_alteracao"].dropna().tolist()
        parecidos = difflib.get_close_matches(termo_busca, todas_alteracoes, n=20, cutoff=0.3)
        resultados = resultados[resultados["nome_da_alteracao"].isin(parecidos)]

    if not resultados.empty:
        # Paginação dos resultados encontrados
        page_size = 5
        total_resultados = len(resultados)
        num_pages = (total_resultados - 1) // page_size + 1 if total_resultados > 0 else 1
        pagina = st.number_input("Página", min_value=1, max_value=num_pages, value=1, step=1)
        start_idx = (pagina - 1) * page_size
        end_idx = start_idx + page_size
        resultados = resultados.iloc[start_idx:end_idx]
        st.write(f"🔎 {len(resultados)} resultado(s) encontrado(s):")
        for _, row in resultados.iterrows():
            with st.expander(f"{row['nome_da_alteracao']}"):
                st.markdown(f"**Achado:** {row['descricao_achado']}")
                st.markdown(f"**Conclusão:** {row.get('conclusao', 'N/A')}")
                if st.button("➕ Inserir no laudo", key=row['nome_da_alteracao']):
                    inserir_automaticamente_em_laudo(row["descricao_achado"], row.get("conclusao", ""))
                    st.success("Frase inserida com sucesso.")
    else:
        st.info("Nenhuma frase encontrada. Digite pelo menos 3 letras para iniciar a busca.")

def painel():
    painel_frases_interativas()
