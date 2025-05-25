
from rapidfuzz import fuzz
import streamlit as st

def fuzzy_match(comando, alvo, limiar=80):
    return fuzz.partial_ratio(comando.lower(), alvo.lower()) >= limiar

def interpretar_comando(comando: str, estado: dict) -> None:
    comando = comando.lower().strip()

    if "teste de voz" in comando or "teste do microfone" in comando:
        st.session_state["voz_detectada"] = "✅ Microfone e reconhecimento de voz funcionando!"
        return

    if any(p in comando for p in ["inserir", "acrescentar", "adicionar"]):
        inserir_em_bloco_por_orgaos(estado, comando)
        return

    # Ativa escuta ativa ao detectar "lili"
    if "lili" in comando:
        estado["lili_status"] = "ativa"
        estado["modo_escuta_ativa"] = True
        try:
            from core.audio import tocar_som
            tocar_som("sons/bip_on.mp3")
        except:
            st.toast("🔔 Escuta ativa iniciada.")
        return

    if fuzzy_match(comando, "abrir frases interativas"):
        estado["pagina"] = "Frases Interativas"
        return

    if comando.startswith("buscar alterações de ") or comando.startswith("buscar alteração de "):
        termo = comando.replace("buscar alterações de ", "").replace("buscar alteração de ", "").strip()
        estado["busca_alteracao"] = termo
        estado["pagina"] = "Frases Interativas"
        return

    if any(fuzzy_match(comando, f"inserir a {ordem} frase") or fuzzy_match(comando, f"escolher a {ordem} frase") for ordem in ["primeira", "segunda", "terceira", "quarta", "quinta"]):
        ordem_index = {"primeira": 0, "segunda": 1, "terceira": 2, "quarta": 3, "quinta": 4}
        for palavra, idx in ordem_index.items():
            if palavra in comando:
                estado["frase_escolhida"] = idx
                break
        return

    if fuzzy_match(comando, "inserir frase selecionada") or fuzzy_match(comando, "adicionar frase escolhida"):
        escolhida = estado.get("frase_escolhida")
        frases = estado.get("frases_filtradas", [])
        if escolhida is not None and escolhida < len(frases):
            frase = frases[escolhida]
            novo_texto = estado.get("texto_laudo", "") + "\n\n" + frase.get("texto", "")
            estado["texto_laudo"] = novo_texto.strip()
        return

    if fuzzy_match(comando, "cancelar") or fuzzy_match(comando, "cancelar comando"):
        estado["lili_status"] = "passiva"
        estado["modo_escuta_ativa"] = False
        estado["transcricao_ao_vivo"] = ""
        try:
            from core.audio import tocar_som
            tocar_som("sons/bip_off.mp3")
        except:
            st.toast("🔕 Escuta ativa cancelada.")
        return

    if not comando:
        return

    if any(fuzzy_match(comando, padrao) for padrao in ["ir para laudos", "abrir laudos", "mostrar laudos"]):
        estado["pagina"] = "Painel de Laudos"
    elif any(fuzzy_match(comando, padrao) for padrao in ["voltar ao início", "retornar para início", "tela inicial"]):
        estado["pagina"] = "Início"
    elif "mostrar frases do sistema" in comando:
        estado["filtro_sistema"] = comando.split("sistema")[-1].strip()
    elif "buscar alteração" in comando:
        estado["busca_alteracao"] = comando.split("alteração")[-1].strip()
    elif any(fuzzy_match(comando, padrao) for padrao in ["salvar frase", "guardar frase", "memorizar"]):
        estado["salvar_frase"] = True
    elif "preencher nome do paciente com" in comando:
        estado["nome_paciente"] = comando.split("com")[-1].strip()
    elif any(fuzzy_match(comando, padrao) for padrao in ["iniciar novo laudo", "novo laudo", "começar laudo"]):
        estado["resetar_laudo"] = True
    elif any(fuzzy_match(comando, padrao) for padrao in ["gerar pdf", "exportar pdf", "salvar como pdf"]):
        estado["gerar_pdf"] = True
    elif fuzzy_match(comando, "mostrar preferências"):
        estado["pagina"] = "Preferências"

    st.toast(f"🎙️ Comando reconhecido: {comando}")

def inserir_em_bloco_por_orgaos(estado, comando):
    import re
    texto = estado.get("texto_laudo", "")
    frase = estado.get("frases_filtradas", [])
    idx = estado.get("frase_escolhida")

    if not texto or idx is None or idx >= len(frase):
        return

    novo = frase[idx]["texto"]

    orgaos = {
        "figado": ["figado", "hepatico"],
        "baço": ["baço", "esplenico"],
        "vesicula": ["vesicula", "biliar"],
        "pancreas": ["pancreas"],
        "rins": ["rins", "rim direito", "rim esquerdo"],
        "adrenal": ["adrenal", "suprarrenal"],
        "estomago": ["estomago"],
        "intestino": ["intestino", "delgado", "grosso"],
        "apendice": ["apendice"],
        "utero": ["utero", "endometrio"],
        "ovario": ["ovario", "ovario direito", "ovario esquerdo"],
        "prostata": ["prostata"],
        "bexiga": ["bexiga"],
        "coluna": ["coluna", "lombar"],
        "pelve": ["pelve", "pelvico"]
    }

    linhas = texto.split("\n")
    for i, linha in enumerate(linhas):
        for orgao, padroes in orgaos.items():
            for padrao in padroes:
                if padrao in comando and padrao in linha.lower():
                    if "inicio" in comando:
                        linhas.insert(i + 1, novo)
                    elif "fim" in comando or "final" in comando or "apos" in comando:
                        linhas.insert(i + 2, novo)
                    estado["texto_laudo"] = "\n".join(linhas)
                    return
