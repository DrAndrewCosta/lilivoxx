import streamlit as st

def painel():
    import streamlit as st

    def render():
        st.header("🎤 Teste de Voz")

        st.write("Este painel simula a ativação do microfone.")
        if st.button("Falar agora"):
            st.info("🎙️ Microfone captando... (simulado)")
            st.session_state["voz_detectada"] = "Exemplo: LILI, gerar laudo"
            st.success(f"Comando reconhecido: {st.session_state['voz_detectada']}")

    voice_test = render
# Versão funcional real do painel de teste de voz
def painel_funcional():
    st.header("🎤 Teste de Voz")
    st.write("Este painel simula a ativação do microfone.")
    if st.button("Falar agora"):
        st.info("🎙️ Microfone captando... (simulado)")
        st.session_state["voz_detectada"] = "Exemplo: LILI, gerar laudo"
        st.success(f"Comando reconhecido: {st.session_state['voz_detectada']}")
