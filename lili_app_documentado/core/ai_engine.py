def analisar_laudo(texto: str):
    """
    Detecta potenciais conflitos entre achados no corpo do texto e na conclusão.
    Retorna lista de inconsistências encontradas.
    """

    conflitos = []

    texto_lower = texto.lower()

    # Exemplo: colecistectomia vs vesícula descrita como presente
    if "colecistectomia" in texto_lower and "vesícula" in texto_lower:
        if any(p in texto_lower for p in ["vesícula com", "vesícula biliar com", "repleção", "conteúdo anecoico"]):
            conflitos.append("Conclusão indica colecistectomia, mas o corpo descreve vesícula como presente e normal.")

    # Exemplo adicional: histerectomia vs útero descrito
    if "histerectomia" in texto_lower and "útero" in texto_lower:
        if "útero com" in texto_lower or "morfologia" in texto_lower:
            conflitos.append("Laudo menciona histerectomia, mas também descreve útero como presente.")

    # Expandir com mais regras conforme necessário
    return texto, conflitos
