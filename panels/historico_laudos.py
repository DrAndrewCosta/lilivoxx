
import streamlit as st
import os
import json
import re

def painel():
    st.title("📚 Histórico de Laudos por Paciente")

    nome_busca = st.text_input("🔍 Nome do paciente")
    if not nome_busca:
        st.info("Digite o nome de um paciente para consultar.")
        return

    nome_limpo = re.sub(r'[^a-zA-Z0-9_]', '_', nome_busca.strip().lower())
    # Buscar todos os arquivos com este nome base
    arquivos = [f for f in os.listdir('historico') if f.startswith(nome_limpo)]
    if not arquivos:
        st.warning("Nenhum histórico encontrado para este paciente.")
        return
    arquivos = sorted(arquivos)
    for arquivo in arquivos:
        with open(os.path.join('historico', arquivo), 'r', encoding='utf-8') as f:
            historico = json.load(f)
        st.markdown(f"### 📁 {arquivo}")
        st.subheader(f"Laudos encontrados: {len(historico)}")
        for idx, entrada in enumerate(historico[::-1]):
            with st.expander(f"📅 {entrada['data']} — {entrada.get('tipo', 'Exame')}"):
                st.markdown(f"**Médico:** {entrada.get('medico', 'N/A')}")
                st.markdown(f"**Data do exame:** {entrada.get('data_exame', 'N/A')}")
                st.text_area("📝 Laudo", value=entrada['laudo'], height=200, key=f"laudo_{arquivo}_{idx}", disabled=True)
                if st.button("🔁 Reutilizar este laudo", key=f"recarregar_{arquivo}_{idx}"):
                    st.session_state["laudo_final"] = entrada['laudo']
                    st.success("✅ Laudo carregado para edição.")
        st.markdown("---")
