import re

def resumir_trecho(texto: str) -> str:
    """
    Resumo clínico baseado em regras heurísticas locais.
    Remove redundâncias e simplifica descrições médicas.
    """

    texto = texto.strip()

    substituicoes = {
        "encontra-se com": "apresenta",
        "paredes finas": "",
        "sem evidência de": "sem",
        "sem sinais de": "sem",
        "sem alterações significativas": "normal",
        "boa repleção": "repleção normal",
        "dentro dos padrões da normalidade": "sem alterações relevantes",
        "nos limites da normalidade": "sem alterações relevantes"
    }

    for original, reduzido in substituicoes.items():
        texto = texto.replace(original, reduzido)

    # Limpar espaços e vírgulas duplicadas
    texto = re.sub(r',\s*,', ',', texto)
    texto = re.sub(r'\s{2,}', ' ', texto).strip()
    texto = re.sub(r' ,', ',', texto)

    return texto
