import streamlit as st
from core.preferences import salvar_config

def painel():
    st.header("⚙️ Preferências do Assistente")

    estilo = st.selectbox("Estilo de linguagem", ["Formal", "Objetivo", "Humanizado"])
    assinatura = st.text_input("Assinatura do Laudo", value="Dr. LILI IA")
    mostrar_feedback = st.checkbox("Mostrar sugestões de IA no final do laudo", value=True)
    modo_voz = st.radio("Modo de escuta por voz", ["Moderno", "Clássico"], index=0)
    st.session_state.setdefault("escuta_continua", True)

    if st.button("Salvar Preferências"):
        config = {
            "estilo": estilo,
            "assinatura": assinatura,
            "mostrar_feedback": mostrar_feedback,
            "modo_voz": modo_voz,
            "escuta_continua": escuta_continua
        }
        st.session_state["modo_voz"] = modo_voz
        st.session_state["escuta_continua"] = escuta_continua
        if salvar_config(config):
            st.success("Preferências salvas com sucesso!")
        else:
            st.error("Erro ao salvar preferências.")
