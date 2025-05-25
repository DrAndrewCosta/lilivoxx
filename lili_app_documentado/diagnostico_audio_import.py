# diagnostico_audio_import.py

try:
    from core.audio import iniciar_escuta_vosk
    print("✅ SUCESSO: iniciar_escuta_vosk importado com sucesso.")
    print("Função carregada:", iniciar_escuta_vosk)
except ImportError as e:
    print("❌ ERRO DE IMPORTAÇÃO:", e)
except Exception as e:
    print("❌ OUTRO ERRO:", e)