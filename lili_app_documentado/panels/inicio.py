import streamlit as st

def painel():
    import streamlit as st
    import datetime
    def render_formulario_inicial():
        st.title("📝 Início - Dados do Exame")

        with st.form("form_dados_exame"):
            nome = st.text_input("👤 Nome do Paciente")
            data_nasc = st.date_input("📅 Data de Nascimento", value=datetime.date(1990, 1, 1))
            data_exame = st.date_input("📆 Data do Exame", value=datetime.date.today())
            medico = st.text_input("🩺 Médico Solicitante", value="Dr(a). LILI IA")
            tipo_exame = st.selectbox("📂 Tipo de Exame / Template", ["Rins", "Abdome", "Tireoide", "Próstata"])

            submitted = st.form_submit_button("✅ Gerar Laudo")

        if submitted:
            st.session_state["nome_paciente"] = nome
            st.session_state["data_nascimento"] = data_nasc.strftime("%Y-%m-%d")
            st.session_state["data_exame"] = data_exame.strftime("%Y-%m-%d")
            st.session_state["medico"] = medico
            st.session_state["tipo_exame"] = tipo_exame

            st.session_state["html_laudo"] = f"""
            <h4>Laudo de Ultrassonografia - {tipo_exame}</h4>
            <p><strong>Paciente:</strong> {nome}</p>
            <p><strong>Data de Nascimento:</strong> {data_nasc.strftime('%d/%m/%Y')}</p>
            <p><strong>Data do Exame:</strong> {data_exame.strftime('%d/%m/%Y')}</p>
            <p><strong>Médico Solicitante:</strong> {medico}</p>
            <p><br><br>Descrição: ___</p>
            <p>Conclusão: ___</p>
            """

            st.success("✅ Dados salvos e laudo gerado!")
            st.info("➡️ Vá até o painel *Assistente* para revisar ou preencher o laudo.")
