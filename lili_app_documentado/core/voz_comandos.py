import streamlit as st
from core.audio import escutar_comando, ouvir_audio_vosk, iniciar_modelo, escutar_loop_ativado

def interpretar_comando(comando):
    st.write(f"🔍 Interpretando comando: {comando}")

def escutar():
    if st.session_state.get("escutando", False):
        st.info("🔁 Já está escutando...")
        return
    st.session_state["escutando"] = True
    st.toast("🎙️ Modo moderno ativado")
    recognizer = iniciar_modelo()
    if recognizer:
        escutar_comando(recognizer, interpretar_comando)
    st.session_state["escutando"] = False

def escutar_classico():
    if st.session_state.get("escutando", False):
        st.info("🔁 Já está escutando...")
        return

    st.session_state["escutando"] = True
    st.toast("🎙️ Modo clássico ativado")
    comando = ouvir_audio_vosk()

    if comando and 'lili' in comando.lower():
        interpretar_comando(comando)
        st.toast(f"✅ Comando reconhecido: {comando}")
        st.session_state["escutando"] = False
        escutar_classico()  # reinicia a escuta após comando
    else:
        st.toast("🕒 Aguardando comando iniciado com LILI...")
        st.session_state["escutando"] = False

def escutar_continuamente():
    if st.session_state.get("escutando", False):
        return
    st.session_state["escutando"] = True
    st.toast("🔁 Escuta contínua ativada")
    escutar_loop_ativado(interpretar_comando)

def escutar_configuravel():
    modo = st.session_state.get("modo_voz", "Moderno")
    continua = st.session_state.get("escuta_continua", False)
    if continua:
        escutar_continuamente()
    elif modo == "Clássico":
        escutar_classico()
    else:
        escutar()
