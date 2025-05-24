import unittest
from core.resumo_clinico import resumir_trecho

class TestResumoClinico(unittest.TestCase):

    def test_resumo_padrao(self):
        entrada = "A vesícula encontra-se com boa repleção, paredes finas, conteúdo anecoico, sem evidência de cálculos."
        esperado = "A vesícula apresenta repleção normal, conteúdo anecoico, sem cálculos."
        resultado = resumir_trecho(entrada)
        self.assertIn("repleção normal", resultado)
        self.assertIn("conteúdo anecoico", resultado)
        self.assertIn("sem cálculos", resultado)

    def test_termos_preservados(self):
        entrada = "Parênquima hepático dentro dos padrões da normalidade."
        resultado = resumir_trecho(entrada)
        self.assertIn("sem alterações relevantes", resultado)

    def test_limpeza_textual(self):
        entrada = "Conteúdo normal , ,  sem sinais de barro biliar."
        resultado = resumir_trecho(entrada)
        self.assertNotIn(",,", resultado)
        self.assertIn("sem barro biliar", resultado)

if __name__ == "__main__":
    unittest.main()
