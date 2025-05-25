import os
import pytest

# Skip este teste se o modelo não estiver presente
@pytest.mark.skipif(
    not os.path.exists("./models/nous-hermes-13b.gguf"),
    reason="Modelo nous-hermes-13b.gguf não encontrado. Ignorado no CI/CD."
)
def test_ia_revisora_funciona():
    from core.ia_revisora import sugerir_reescrita
    entrada = "Paciente com dor abdominal"
    saida = sugerir_reescrita(entrada)
    assert isinstance(saida, str)
    assert len(saida) > 0