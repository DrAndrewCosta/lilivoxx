import streamlit as st

def painel():
    import streamlit as st
    import logging

    def render():
        st.header("📥 Importar Materiais")
        file = st.file_uploader("Carregar arquivo de texto:", type=["txt", "md"])
        if file:
            try:
                content = file.read().decode("utf-8")
            except Exception as e:
                logging.error(f'Erro ao ler arquivo importado: {e}')
                st.error('Não foi possível ler o arquivo.')
                return
            st.text_area("Conteúdo:", value=content, height=300)
            if st.button("Usar como Laudo Atual"):
                st.session_state["texto_laudo"] = content
                st.success("Conteúdo carregado.")
                logging.info(f'Arquivo importado: {file.name}')

    importation = render