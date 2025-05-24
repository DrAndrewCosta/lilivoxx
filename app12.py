
import streamlit as st
st.set_page_config(page_title="LILI App", layout="wide")
from panels.cadastro_frases import render as cadastro_painel
from panels import (
    painel_cabecalho_laudo,
    assistant_painel,
    preferencias_painel,
    importar_paciente,
    gerar_laudo,
    laudos_painel,
    inicio,
    importation,
    dinamico,
    voice_test,
    painel_frases_interativas,
    ia_dashboard,
)
from core import voz_comandos
from voz_inteligente import interpretar_comando
from core.conclusao_automatica import conclusao_padrao_por_exame
import streamlit.components.v1 as components

voz_comandos.escutar()
st.toast('🎙️ Escuta de voz ativada... Diga: LILI + comando')
# -------------------- CONFIGURAÇÕES GERAIS --------------------

def render_comando_voz_sidebar():
    st.sidebar.markdown("## 🎙️ Comandos por Voz")
    st.sidebar.markdown("Diga comandos como 'reescreva', 'clarear texto', 'resuma', 'amplie'.")
    st.sidebar.markdown("Você também pode dizer: 'desfazer', 'limpar', ou 'salvar laudo'.")
    st.sidebar.markdown(":memo: Fale 'abrir assistente' para abrir a IA Dashboard.")

def interpretar_acao_voz(acao):
    comandos = {
        "gerar laudo": "Laudos",
        "importar paciente": "Importação",
        "abrir assistente": "IA Dashboard"
    }
    for chave, destino in comandos.items():
        if chave in acao.lower():
            st.session_state["pagina"] = destino
            st.rerun()

# -------------------- ESTADO INICIAL --------------------
if "modo_escuta_ativa" not in st.session_state:
    st.session_state["modo_escuta_ativa"] = True

if "pagina" not in st.session_state:
    st.session_state["pagina"] = "Cadastro Inteligente"

comando_ativacao = "lili"

# -------------------- COMANDO POR VOZ --------------------
def ativar_escuta_por_comando(entrada_texto):
    if st.session_state["modo_escuta_ativa"]:
        return True
    if comando_ativacao in entrada_texto.lower():
        st.session_state["modo_escuta_ativa"] = True
        return True
    return False

def verificar_conflitos():
    conflitos = st.session_state.get("ultimos_conflitos", [])
    if conflitos:
        with st.expander("⚠️ Conflitos detectados no preenchimento por voz"):
            for conflito in conflitos:
                st.error(conflito)

PAGINAS = {
    "Cadastro Inteligente": painel_cabecalho_laudo,
    "Assistente": assistant_painel,
    "Preferências": preferencias_painel,
    "Importar Paciente": importar_paciente,
    "Gerar Laudo": gerar_laudo,
    "Importar Frases": importation,
    "Teste de Voz": voice_test,
    "IA Dashboard": ia_dashboard,
    "Todos os Laudos": laudos_painel,
    "Cadastro de Frases": cadastro_painel,
    "Início": inicio,
    "Frases Interativas": painel_frases_interativas,
}

def render_sidebar():
    st.sidebar.title("🔷 Navegação")
    pagina = st.sidebar.radio("Ir para", list(PAGINAS.keys()))
    st.session_state["pagina"] = pagina
    render_comando_voz_sidebar()
    st.sidebar.markdown("---")
    if st.sidebar.button("🎤 Ativar Microfone"):
        voz_comandos.escutar_configuravel()

# -------------------- PERMISSÃO DO MICROFONE --------------------
def requisitar_permissao_microfone():
    components.html(
        """
        <script>
        (async () => {
            if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
                alert("Seu navegador não suporta captura de áudio.");
                return;
            }
            try {
                await navigator.mediaDevices.getUserMedia({ audio: true });
                console.log("🎤 Permissão de microfone concedida.");
            } catch (err) {
                alert("⚠️ O microfone está bloqueado. Por favor, ative nas configurações do navegador.");
            }
        })();
        </script>
        """,
        height=0
    )

# -------------------- MAIN --------------------
def main():

    # Garante escuta contínua ativa entre painéis
    if st.session_state.get("escuta_continua", True):
        if "escutando" not in st.session_state:
            import threading
            st.session_state["escutando"] = True
            threading.Thread(target=voz_comandos.escutar, daemon=True).start()
    requisitar_permissao_microfone()
    voz_comandos.escutar()
    st.toast('🎙️ Escuta de voz ativada... Diga: LILI + comando')
    with st.sidebar:
        render_sidebar()
    verificar_conflitos()

    # Feedback visual do status da Lili
    lili_status = st.session_state.get("lili_status", "passiva")
    status_text = {
        "passiva": "🎧 Lili em escuta passiva",
        "ativa": "🎙️ Lili em escuta ativa",
        "executando": "⚙️ Lili processando comando"
    }.get(lili_status, "🔈 Status desconhecido")
    st.markdown(f"<div style='background:#f7f7f7; padding:6px 12px; color:#444; font-size:14px; border-bottom:1px solid #ccc;'>{status_text}</div>", unsafe_allow_html=True)


    # Mostrar transcrição ao vivo discretamente
    transcricao = st.session_state.get("transcricao_ao_vivo", "")
    if transcricao:
        st.markdown(f"<div style='position:fixed; bottom:0; width:100%; color:#888; background:#f0f0f0; padding:5px 15px; font-size:13px;'>🎙️ {transcricao}</div>", unsafe_allow_html=True)
    # Interpretação global do comando de voz
    comando_voz = st.session_state.get("ultimo_comando", "")
    if comando_voz:
        interpretar_comando(comando_voz, st.session_state)
        st.session_state["ultimo_comando"] = ""
    pagina_atual = st.session_state.get("pagina", "Cadastro Inteligente")
    PAGINAS[pagina_atual]()



    # Rodapé de status da Lili
    if "lili_status" in st.session_state and st.session_state["lili_status"]:
        with st.container():
            st.markdown(
                f"<div style='position:fixed; bottom:0; width:100%; background:#f0f2f6; color:#333; padding:8px 16px; font-size:14px; text-align:center; border-top:1px solid #ccc;'>"
                f"{st.session_state['lili_status']}"
                "</div>",
                unsafe_allow_html=True
            )
if __name__ == "__main__":
    main()
