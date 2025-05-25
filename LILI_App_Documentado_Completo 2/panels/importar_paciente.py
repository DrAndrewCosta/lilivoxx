import streamlit as st

def painel():
    import streamlit as st

    def importar_paciente():
        st.header("📁 Importar Paciente")

        nome = st.text_input("Nome do Paciente")
        data_nascimento = st.date_input("Data de Nascimento")
        tipo_exame = st.selectbox("Tipo de Exame", ["Rins", "Abdome", "Próstata", "Tireoide"])
        data_exame = st.date_input("Data do Exame")
        medico = st.text_input("Médico Solicitante", value="Dr. LILI IA")

        if st.button("Carregar Dados"):
            st.session_state["nome_paciente"] = nome
            st.session_state["data_nascimento"] = data_nascimento.strftime("%Y-%m-%d")
            st.session_state["tipo_exame"] = tipo_exame
            st.session_state["data_exame"] = data_exame.strftime("%Y-%m-%d")
            st.session_state["medico"] = medico
            st.success("Paciente carregado com sucesso!")

        if "nome_paciente" in st.session_state:
            st.markdown(f"**Paciente:** {st.session_state['nome_paciente']}")
            st.markdown(f"**Nascimento:** {st.session_state['data_nascimento']}")
            st.markdown(f"**Exame:** {st.session_state['tipo_exame']}")
            st.markdown(f"**Data do Exame:** {st.session_state['data_exame']}")
            st.markdown(f"**Médico:** {st.session_state['medico']}")