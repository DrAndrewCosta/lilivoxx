
import streamlit as st
import pandas as pd
import os
from datetime import datetime

def gerar_conclusao(estrutura, alteracao):
    return f"Achado sugestivo de {alteracao.lower()} em {estrutura.lower()}."

def gerar_comando(acao):
    return f"adicionar_{acao.lower().replace(' ', '_').replace('ç', 'c')}"

def sugerir_tags(alteracao):
    palavras = alteracao.lower()
    tags = []
    if "cisto" in palavras: tags.append("benigno")
    if "nódulo" in palavras: tags.append("nodulo")
    if "tumor" in palavras: tags.append("suspeito")
    if "normal" in palavras or "habitual" in palavras: tags.append("normal")
    if "hemangioma" in palavras: tags.append("benigno")
    return ", ".join(tags)

def completar_colunas_faltantes(df):
    if "Conclusão" not in df:
        df["Conclusão"] = df.apply(lambda row: gerar_conclusao(row["Estrutura"], row["Alteração"]), axis=1)
    if "Comando de Voz" not in df:
        df["Comando de Voz"] = df["Alteração"].apply(gerar_comando)
    if "Tags" not in df:
        df["Tags"] = df["Alteração"].apply(sugerir_tags)
    return df

def render():
    st.title("📥 Importar Novas Frases Clínicas em Bloco")

    uploaded_file = st.file_uploader("Enviar arquivo CSV com novas frases (separado por '|')", type="csv")

    if uploaded_file:
        try:
            df_novo = pd.read_csv(uploaded_file, sep="|")
            df_novo.columns = df_novo.columns.str.strip()

            obrigatorios = ["Alteração", "Frase Clínica", "Estrutura"]
            faltando = [col for col in obrigatorios if col not in df_novo.columns]
            if faltando:
                st.error(f"O arquivo está faltando as colunas obrigatórias: {', '.join(faltando)}")
                return

            st.subheader("🔍 Pré-visualização das novas frases")
            st.dataframe(df_novo)

            df_novo = completar_colunas_faltantes(df_novo)

            if st.button("✅ Importar e adicionar ao frases.csv"):
                frases_path = "frases.csv"
                backup_path = f"frases_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
                if os.path.exists(frases_path):
                    with open(frases_path, "rb") as original, open(backup_path, "wb") as backup:
                        backup.write(original.read())
                    df_existente = pd.read_csv(frases_path, sep="|")
                    df_existente.columns = df_existente.columns.str.strip()
                else:
                    df_existente = pd.DataFrame(columns=df_novo.columns)

                df_final = pd.concat([df_existente, df_novo], ignore_index=True)
                df_final.to_csv(frases_path, sep="|", index=False)
                st.success("Frases importadas com sucesso! Backup criado.")
                st.info(f"Backup salvo como: {backup_path}")
        except Exception as e:
            st.error(f"Erro ao processar o arquivo: {e}")
