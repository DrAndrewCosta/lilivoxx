import re

def gerar_conclusao(alteracao, frase):
    frase = frase.strip().lower()
    alteracao = alteracao.strip().lower()
    return f"A presença de {alteracao} sugere alteração compatível com {frase}."

def gerar_comando(frase):
    comando = frase.lower()
    comando = re.sub(r"[^a-zA-Z0-9\s]", "", comando)
    comando = re.sub(r"\s+", "_", comando.strip())
    return comando

def gerar_tags(frase):
    frase = frase.lower()
    palavras = re.findall(r'\b[a-zA-Z]{4,}\b', frase)
    return ",".join(sorted(set(palavras)))