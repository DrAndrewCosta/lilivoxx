
from pathlib import Path
from llama_cpp import Llama
from tinydb import TinyDB, Query
import os

MODELO_PATH = Path("models/nous-hermes-13b.gguf")
llm = Llama(model_path=str(MODELO_PATH), n_ctx=2048, n_threads=4)

db_path = os.path.join("db", "usuarios.json")
os.makedirs(os.path.dirname(db_path), exist_ok=True)
db = TinyDB(db_path)
Usuario = Query()

def registrar_aplicacao(usuario: str, tipo: str, original: str, sugestao: str):
    db.insert({
        "usuario": usuario,
        "tipo": tipo,
        "original": original,
        "sugestao": sugestao,
    })

def obter_preferencias_de_estilo(usuario: str) -> dict:
    docs = db.search(Usuario.usuario == usuario)
    palavras = {}
    for doc in docs:
        for palavra in doc['sugestao'].split():
            palavra = palavra.strip(",.")
            palavras[palavra] = palavras.get(palavra, 0) + 1
    palavras_mais_comuns = sorted(palavras.items(), key=lambda x: -x[1])[:10]
    return {"palavras_comuns": palavras_mais_comuns}

def ajustar_sugestao_com_perfil(sugestao: str, usuario: str) -> str:
    estilo = obter_preferencias_de_estilo(usuario)
    for palavra, _ in estilo["palavras_comuns"]:
        if palavra in sugestao:
            sugestao = sugestao.replace(palavra, palavra.upper())
    return sugestao

def gerar(texto: str, tipo: str) -> str:
    prompt_map = {
        "reescrita": f'''Reescreva com clareza médica:\n"{texto}"\n\nReescrita:''',
        "resumo": f'''Resuma tecnicamente:\n"{texto}"\n\nResumo:''',
        "clareza": f'''Torne o texto mais compreensível:\n"{texto}"\n\nTexto claro:''',
        "ampliar": f'''Amplie com detalhes clínicos:\n"{texto}"\n\nVersão ampliada:''',
    }
    prompt = prompt_map.get(tipo)
    if not prompt:
        return "[Erro: tipo inválido]"
    resposta = llm(prompt, max_tokens=300, stop=["\n"], echo=False)
    return resposta["choices"][0]["text"].strip()

def sugerir_reescrita(texto): return gerar(texto, "reescrita")
def resumir_trecho(texto): return gerar(texto, "resumo")
def clarear_texto(texto): return gerar(texto, "clareza")
def ampliar_texto(texto): return gerar(texto, "ampliar")
