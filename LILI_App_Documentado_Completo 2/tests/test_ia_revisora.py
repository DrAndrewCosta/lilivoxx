import unittest
from core.ia_revisora import sugerir_reescrita, localizar_trecho_por_comando

class TestIARevisora(unittest.TestCase):

    def test_sugerir_reescrita(self):
        entrada = "Exame dentro da normalidade."
        esperado = "Exame nos limites da normalidade."
        resultado = sugerir_reescrita(entrada)
        self.assertIn("nos limites da normalidade", resultado)

    def test_localizar_trecho_por_comando_textual(self):
        laudo = (
            "Parênquima hepático homogêneo.\n"
            "Vesícula com boa repleção e conteúdo anecoico homogeneo, sem cálculos.\n"
            "Volume prostático estimado em ___ g."
        )
        comando = "próstata"
        resultado = localizar_trecho_por_comando(comando, laudo)
        self.assertIn("Volume prostático", resultado)

if __name__ == "__main__":
    unittest.main()
