from gpt4all import GPT4All

# Modelo .gguf oficial em uso
modelo = GPT4All("nous-hermes-13b.gguf", model_path="./models", allow_download=False)

def sugerir_reescrita(texto):
    prompt = f"Reescreva o seguinte trecho com linguagem médica clara e objetiva, sem mudar o sentido:\n\n{texto}\n\nReescrita:"
    resposta = modelo.prompt(prompt, max_tokens=300)
    return resposta.strip()

def localizar_trecho_por_comando(comando, texto):
    prompt = f"Com base no comando '{comando}', localize e retorne o trecho mais relevante do seguinte texto:\n\n{texto}\n\nTrecho correspondente:"
    resposta = modelo.prompt(prompt, max_tokens=200)
    return resposta.strip()