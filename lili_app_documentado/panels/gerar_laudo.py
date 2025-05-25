import streamlit as st
from export import exportar_laudo_docx, exportar_laudo_pdf

def render():
    st.header("📝 Gerador de Laudos")

    if "texto_laudo" not in st.session_state:
        st.session_state["texto_laudo"] = ""

    texto = st.text_area("Escreva ou edite o laudo:", key="texto_laudo", height=400)

    nome = st.text_input("Nome do Paciente")
    tipo_exame = st.text_input("Tipo de Exame", value="Rins")
    data_exame = st.date_input("Data do Exame")
    medico = st.text_input("Médico Responsável", value="Dr. LILI IA")
    data_nascimento = st.date_input("Data de Nascimento", key="data_nasc")

    template_path = "./templates/rins_melhorado.docx"

    if st.button("💾 Finalizar e Exportar Laudo"):
        caminho_docx = exportar_laudo_docx(
            texto=texto,
            nome_paciente=nome,
            tipo_exame=tipo_exame,
            data_exame_iso=data_exame.strftime("%Y-%m-%d"),
            medico=medico,
            template_path=template_path,
            nome_arquivo="laudo_final.docx",
            data_nascimento=data_nascimento.strftime("%Y-%m-%d")
        )

        caminho_pdf = exportar_laudo_pdf(texto, nome_arquivo="laudo_final.pdf")

        st.success("Laudo exportado com sucesso!")

        with open(caminho_docx, "rb") as docx_file:
            st.download_button("📄 Baixar Laudo DOCX", docx_file, file_name="laudo_final.docx")

        with open(caminho_pdf, "rb") as pdf_file:
            st.download_button("📄 Baixar Laudo PDF", pdf_file, file_name="laudo_final.pdf")

painel = render
