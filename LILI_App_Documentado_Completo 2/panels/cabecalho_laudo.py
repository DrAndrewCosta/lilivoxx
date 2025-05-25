import streamlit as st
import datetime

def painel():
    st.title("📋 Cadastro de Exame com Pré-visualização Inteligente")

    st.subheader("👤 Dados do Paciente")
    nome = st.text_input("Nome do Paciente")

    # Simula campo vazio com um checkbox
    data_nasc_str = st.text_input("Data de Nascimento (DD/MM/AAAA)")
    try:
        data_nasc = datetime.datetime.strptime(data_nasc_str, "%d/%m/%Y").date()
        data_nasc_valida = True
    except:
        data_nasc = None
        data_nasc_valida = False

    data_exame = st.date_input(
        "Data do Exame",
        value=datetime.date.today(),
        format="DD/MM/YYYY"
    )

    medico = st.text_input("Médico Solicitante", value="Dr(a). LILI IA")

    if len(nome.strip()) >= 10 and data_exame and data_nasc_valida:
        st.success("✅ Dados essenciais preenchidos.")
        tipos = {
            "Rins": "Paciente com rins de morfologia preservada, sem evidência de litíase ou hidronefrose.",
            "Abdome": "Exame abdominal dentro dos limites da normalidade.",
            "Tireoide": "Parênquima tireoidiano homogêneo, sem nódulos evidentes.",
            "Próstata": "Próstata com volume dentro dos parâmetros normais, sem alterações significativas."
        }
        tipo_exame = st.selectbox("📂 Tipo de Exame / Template", [""] + list(tipos.keys()))
    else:
        tipo_exame = None
        if nome and len(nome.strip()) < 10:
            st.warning("⚠️ O nome do paciente deve ter pelo menos 10 caracteres.")
        if not data_nasc_valida and data_nasc_str:
            st.warning("⚠️ Data de nascimento inválida. Use o formato DD/MM/AAAA.")
        elif not data_nasc_str:
            st.info("🔒 Preencha o nome (mín. 10 caracteres) e a data de nascimento para liberar os templates.")

    if tipo_exame:
        texto_base = tipos[tipo_exame]

        st.subheader("📝 Edição e Visualização do Laudo")
        col1, col2 = st.columns(2)

        with col1:
            laudo_editado = st.text_area("✍️ Edite o Laudo", value=texto_base, height=200)

        with col2:
            st.markdown("📄 **Pré-visualização**")
            st.markdown(laudo_editado)

        if st.button("✅ Salvar Laudo"):
            st.session_state["laudo_final"] = laudo_editado
            st.session_state["nome_paciente"] = nome
            st.session_state["data_nascimento"] = data_nasc.strftime("%d/%m/%Y") if data_nasc else ""
            st.session_state["data_exame"] = data_exame.strftime("%d/%m/%Y")
            st.session_state["medico"] = medico
            st.session_state["tipo_exame"] = tipo_exame
            st.success("✅ Laudo salvo com sucesso!")