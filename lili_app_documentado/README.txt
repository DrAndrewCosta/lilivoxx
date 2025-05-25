
# LILI App - Versão Final com Texto Puro

✅ Assistente de Laudos Médicos com comandos por voz, IA local e exportação profissional.

## Recursos:
- Preenchimento automático por voz
- IA local integrada (Hermes 13B - llama.cpp)
- Reescrita, clareza, resumo e expansão por IA
- Exportação para DOCX e PDF
- Abre automaticamente no Word (macOS)
- Textos 100% livres de HTML para máxima robustez

## Como usar:

1. Instale dependências:
   pip install streamlit python-docx fpdf llama-cpp-python vosk

2. Certifique-se de ter os modelos:
   - /models/nous-hermes-13b.gguf
   - /models/vosk-model-small-pt-0.3

3. Execute:
   streamlit run app.py
