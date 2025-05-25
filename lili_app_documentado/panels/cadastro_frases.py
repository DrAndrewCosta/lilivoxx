import os
import shutil
import pandas as pd
import streamlit as st
from datetime import datetime
from core.utils import gerar_conclusao, gerar_comando, gerar_tags

ARQUIVO_CSV = "frases.csv"
COLUNAS_OBRIGATORIAS = ["Alteração", "Frase Clínica", "Estrutura"]

def salvar_csv(df):
    backup = f"backup_frases_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    shutil.copy(ARQUIVO_CSV, backup) if os.path.exists(ARQUIVO_CSV) else None
    df.to_csv(ARQUIVO_CSV, index=False)
    st.success(f"Frases salvas com sucesso! Backup criado: {backup}")

def carregar_frases():
    if "frases_csv" not in st.session_state or st.session_state["frases_csv"] is None:
        if os.path.exists(ARQUIVO_CSV):
            st.session_state["frases_csv"] = pd.read_csv(ARQUIVO_CSV)
        else:
            st.session_state["frases_csv"] = pd.DataFrame(columns=COLUNAS_OBRIGATORIAS + ["Conclusão", "Comando de Voz", "Tags"])
    return st.session_state["frases_csv"]

def painel_importar_csv():
    st.subheader("📥 Importar Frases via CSV")
    arquivo = st.file_uploader("Selecione um arquivo CSV", type="csv")
    if arquivo:
        try:
            novo_df = pd.read_csv(arquivo)
            if not all(col in novo_df.columns for col in COLUNAS_OBRIGATORIAS):
                st.error(f"O CSV deve conter as colunas obrigatórias: {COLUNAS_OBRIGATORIAS}")
                return

            novo_df["Conclusão"] = novo_df.apply(lambda row: gerar_conclusao(row["Alteração"], row["Frase Clínica"]), axis=1)
            novo_df["Comando de Voz"] = novo_df.apply(lambda row: gerar_comando(row["Frase Clínica"]), axis=1)
            novo_df["Tags"] = novo_df.apply(lambda row: gerar_tags(row["Frase Clínica"]), axis=1)

            st.write("📋 Pré-visualização das frases importadas:")
            st.dataframe(novo_df)

            if st.button("✅ Adicionar ao banco de frases"):
                df_atual = carregar_frases()
                df_atual = pd.concat([df_atual, novo_df], ignore_index=True).drop_duplicates()
                st.session_state["frases_csv"] = df_atual
                salvar_csv(df_atual)
        except Exception as e:
            st.error(f"Erro ao processar o arquivo: {e}")

def painel_cadastro_manual():
    st.subheader("🧾 Cadastro Manual de Frases")
    df = carregar_frases()

    with st.form("formulario_frase"):
        alteracao = st.text_input("Alteração")
        frase_clinica = st.text_area("Frase Clínica")
        estrutura = st.text_input("Estrutura")

        if st.form_submit_button("➕ Adicionar"):
            if not alteracao or not frase_clinica or not estrutura:
                st.warning("Por favor, preencha todos os campos obrigatórios.")
            else:
                nova = {
                    "Alteração": alteracao,
                    "Frase Clínica": frase_clinica,
                    "Estrutura": estrutura,
                    "Conclusão": gerar_conclusao(alteracao, frase_clinica),
                    "Comando de Voz": gerar_comando(frase_clinica),
                    "Tags": gerar_tags(frase_clinica)
                }
                df = pd.concat([df, pd.DataFrame([nova])], ignore_index=True)
                st.session_state["frases_csv"] = df
                salvar_csv(df)

    st.markdown("### ✏️ Editar ou Excluir Frases")
    if not df.empty:
        for idx, row in df.iterrows():
            with st.expander(f"{row['Frase Clínica']}"):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.text_area("Editar Frase Clínica", value=row["Frase Clínica"], key=f"edit_{idx}")
                with col2:
                    if st.button("🗑️ Excluir", key=f"del_{idx}"):
                        df.drop(index=idx, inplace=True)
                        st.session_state["frases_csv"] = df.reset_index(drop=True)
                        salvar_csv(st.session_state["frases_csv"])
                        st.experimental_rerun()

def render():
    st.title("📋 Cadastro e Importação de Frases")
    aba = st.radio("Escolha uma opção", ["📥 Importar CSV", "🧾 Cadastro Manual"], horizontal=True)
    if aba == "📥 Importar CSV":
        painel_importar_csv()
    else:
        painel_cadastro_manual()

def painel():
    render()
