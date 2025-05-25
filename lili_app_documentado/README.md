# 🧠 LILI App - Assistente com IA e Voz

Aplicativo web interativo para laudos médicos com suporte a:
- Comandos de voz (offline, com Vosk)
- Geração automática de texto
- Edição interativa via assistente
- Templates de laudos customizáveis

## 🚀 Como executar

1. Instale os requisitos:

```bash
pip install -r requirements.txt
```

2. Execute o app:

```bash
streamlit run app12.py
```

3. Use o menu lateral para navegar entre os painéis.

## 📁 Estrutura de Diretórios

- `panels/` – Painéis Streamlit modulares
- `core/` – Lógica de IA, voz e utilitários
- `resources/` – Arquivos de áudio, frases e templates
- `models/` – Modelo de voz offline Vosk (pt-br)
- `config/` – Configurações da aplicação