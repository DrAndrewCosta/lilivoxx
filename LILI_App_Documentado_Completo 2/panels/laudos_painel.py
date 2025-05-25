import streamlit as st

def painel():
    from core.audio import ler_em_voz_alta
    import logging
    import streamlit as st
    from core.ai_engine import analisar_laudo


    def render():
        st.header("⚠️ Conflitos no Laudo")
        texto = st.session_state.get("texto_laudo", "")

        if not texto.strip():
            st.info("Nenhum texto disponível para análise.")
            return

        _, contradicoes = analisar_laudo(texto)

        if not contradicoes:
            st.success("Nenhum conflito encontrado.")
            return

        logging.info(f"{len(contradicoes)} conflito(s) detectado(s).")
        for item in contradicoes:
            st.warning(f"Conflito: {item}")


    laudos_painel = render