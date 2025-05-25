import pytest
from lili_app_documentado.voz_inteligente import interpretar_comando

def test_comando_valido_com_lili():
    estado = {"lili_status": "passiva"}

    interpretar_comando("LILI", estado)
    assert estado["lili_status"] == "ativa"

    interpretar_comando("abrir assistente", estado)
    assert estado.get("pagina") == "IA Dashboard"
    assert estado["lili_status"] == "passiva"

def test_comando_sem_lili():
    estado = {"lili_status": "passiva"}

    interpretar_comando("abrir assistente", estado)
    assert "pagina" not in estado
    assert estado["lili_status"] == "passiva"

def test_resetar_laudo():
    estado = {"lili_status": "passiva"}

    interpretar_comando("LILI", estado)
    assert estado["lili_status"] == "ativa"

    interpretar_comando("iniciar novo laudo", estado)
    assert estado.get("resetar_laudo") is True
    assert estado["lili_status"] == "passiva"

def test_gerar_pdf():
    estado = {"lili_status": "passiva"}

    interpretar_comando("LILI", estado)
    assert estado["lili_status"] == "ativa"

    interpretar_comando("salvar como pdf", estado)
    assert estado.get("gerar_pdf") is True
    assert estado["lili_status"] == "passiva"