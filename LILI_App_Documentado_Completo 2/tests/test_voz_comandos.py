
import pytest
import streamlit as st
from voz_inteligente import interpretar_comando

@pytest.fixture(autouse=True)
def setup_session_state():
    # Garante que o session_state esteja limpo para cada teste
    st.session_state.clear()
    yield
    st.session_state.clear()

def test_comando_valido_com_lili():
    comando = "LILI, abrir assistente"
    estado = {}
    interpretar_comando(comando, estado)
    assert estado.get("pagina") == "IA Dashboard"

def test_comando_sem_lili():
    comando = "abrir assistente"
    estado = {}
    interpretar_comando(comando, estado)
    assert estado.get("pagina") == "IA Dashboard"

def test_comando_desconhecido():
    comando = "ligar luz"
    estado = {}
    interpretar_comando(comando, estado)
    assert estado == {}
