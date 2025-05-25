import streamlit as st
import datetime

def painel():
    st.title("📋 Cadastro de Exame com Template Inteligente")

    nome = st.text_input("👤 Nome do Paciente")
    data_exame = st.date_input("📅 Data do Exame", value=datetime.date.today(), format="DD/MM/YYYY")

    if nome.strip():
        st.success("✅ Nome do paciente preenchido.")
    else:
        st.warning("Preencha o nome do paciente.")

    if nome.strip() and data_exame:
        tipo_exame = st.selectbox("📂 Tipo de Exame / Template", ["", "Rins", "Abdome", "Tireoide", "Próstata"])

        if tipo_exame:
            # Dados de exemplo para cada template
            templates = {
                "Rins": "O rim direito mede {rim_direito} cm e apresenta {descricao_direito}.",
                "Abdome": "O exame abdominal revela {descricao_abdome}.",
                "Tireoide": "A glândula tireoide tem dimensões {dimensoes} com {achados}.",
                "Próstata": "A próstata mede {tamanho_prostata} cm³ com {observacoes}."
            }

            template = templates[tipo_exame]
            st.session_state["template_selecionado"] = template
            st.session_state["tipo_exame"] = tipo_exame

            st.success("➡️ Template carregado. Preencha os campos abaixo:")

            # Detectar placeholders
            campos = [campo.strip("{}") for campo in template.split() if campo.startswith("{")]
            valores = {}

            for campo in campos:
                valores[campo] = st.text_input(f"{campo.replace('_', ' ').capitalize()}")

            if st.button("✅ Gerar Laudo Final"):
                try:
                    laudo_final = template.format(**valores)
                    st.session_state["laudo_final"] = laudo_final
                    st.success("📝 Laudo gerado com sucesso:")
                    st.markdown(laudo_final)
                except KeyError as e:
                    st.error(f"Campo faltando: {e}")
    else:
        st.info("🔒 O menu de templates será liberado após preencher nome e data do exame.")