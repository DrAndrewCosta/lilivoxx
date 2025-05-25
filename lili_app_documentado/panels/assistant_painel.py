import streamlit as st
import re
from core.audio import ler_em_voz_alta

def painel():
    def assistant_painel():
        comando_voz = st.session_state.get("voz_detectada", "")
        if comando_voz:
            st.info(f"🎤 Comando por voz detectado: {comando_voz}")
            if st.checkbox("🔊 Ler comando em voz alta"):
                ler_em_voz_alta(comando_voz)

        st.title("🤖 Assistente de Preenchimento por Voz")
        html_laudo = st.session_state.get("html_laudo", "")
        if not html_laudo:
            st.warning("⚠️ Nenhum laudo carregado. Gere um laudo primeiro ou vá para o painel de geração.")
            st.stop()

        # Regex para encontrar todos os campos do tipo ___
        campos = list(re.finditer(r'_{3,}', html_laudo))

        if "campos_substituidos" not in st.session_state:
            st.session_state["campos_substituidos"] = []

        if st.button("🔄 Redefinir campos"):
            st.session_state["campos_substituidos"] = []

        campos_pendentes = [c for i, c in enumerate(campos) if i not in st.session_state["campos_substituidos"]]

        if campos_pendentes:
            st.info(f"Há {len(campos_pendentes)} campo(s) para preenchimento.")
            campo_atual = campos_pendentes[0]
            valor = st.text_input("🖊️ Preencha o campo encontrado no laudo")

            if st.button("✅ Inserir"):
                inicio, fim = campo_atual.start(), campo_atual.end()
                novo_html = html_laudo[:inicio] + valor + html_laudo[fim:]
                st.session_state["html_laudo"] = novo_html
                st.session_state["campos_substituidos"].append(campos.index(campo_atual))
                st.experimental_rerun()
        else:
            st.success("✅ Todos os campos foram preenchidos!")

        st.markdown("### 📄 Pré-visualização do Laudo:")
        st.markdown(st.session_state["html_laudo"], unsafe_allow_html=True)

    # Chama a função interna
    assistant_painel()
