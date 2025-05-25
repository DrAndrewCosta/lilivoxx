import streamlit as st

def painel():

    import streamlit as st
    from datetime import datetime

    def render():
        st.title("🧠 Painel de Controle da IA")

        # Simula histórico local
        historico = st.session_state.get("historico_ia", [])

        st.subheader("📋 Histórico de Sugestões")
        if not historico:
            st.info("Nenhuma sugestão registrada ainda.")
        else:
            for item in reversed(historico[-10:]):  # mostrar as 10 últimas
                with st.expander(f"{item['tipo'].capitalize()} — {item['timestamp']}"):
                    st.markdown(f"**Trecho original:**\n\n{item['original']}")
                    st.markdown(f"**Sugestão da IA:**\n\n{item['sugestao']}")
                    st.markdown(f"**Status:** `{item['status']}`")

        st.divider()
        st.subheader("⚙️ Configurações da IA")
        st.checkbox("Ativar detecção de conflitos em tempo real", key="ia_conflitos", value=True)
        st.checkbox("Permitir reescrita automática com confirmação", key="ia_reescrita", value=True)
        st.checkbox("🔊 Ativar leitura em voz alta das sugestões", key="voz_alta", value=st.session_state.get("voz_alta", True))

        st.divider()
        st.subheader("📊 Estatísticas")
        total = len(historico)
        aplicadas = len([h for h in historico if h['status'] == "aplicado"])
        st.markdown(f"- Sugestões feitas: **{total}**")
        st.markdown(f"- Sugestões aplicadas: **{aplicadas}**")
        if total:
            taxa = (aplicadas / total) * 100
            st.markdown(f"- Taxa de aceitação: **{taxa:.1f}%**")


    ia_dashboard = render