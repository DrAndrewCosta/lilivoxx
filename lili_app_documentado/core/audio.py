import pyttsx3

def log_evento_lili(tipo, conteudo):
    from datetime import datetime
    now = datetime.now().strftime("%H:%M:%S")
    print(f"[{now}] [{tipo.upper()}] {conteudo}")
import simpleaudio as sa
import os
import queue
import time
import json
import sounddevice as sd
from vosk import Model, KaldiRecognizer
import streamlit as st

def tocar_som(caminho):
    try:
        wave_obj = sa.WaveObject.from_wave_file(caminho)
        play_obj = wave_obj.play()
        play_obj.wait_done()
    except Exception as e:
        print(f"[ERRO] ao tocar som: {e}")

def ler_em_voz_alta(texto):
    try:
        engine = pyttsx3.init()
        engine.say(texto)
        engine.runAndWait()
    except Exception as e:
        print(f"Erro ao tentar falar: {e}")

def iniciar_modelo():
    try:
        model_path = "models/vosk-model-small-pt-0.3"
        if not os.path.exists(model_path):
            print("Modelo Vosk não encontrado.")
            return None
        model = Model(model_path)
        recognizer = KaldiRecognizer(model, 16000)
        recognizer.SetWords(True)
        return recognizer
    except Exception as e:
        print(f"Erro ao iniciar modelo: {e}")
        return None

def escutar_comando(recognizer, comando_callback, timeout=10):
    try:
        audio_q = queue.Queue()
        def audio_callback(indata, frames, time_info, status):
            if status:
                print(status)
            audio_q.put(bytes(indata))

        with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                               channels=1, callback=audio_callback):
            inicio = time.time()
            while True:
                if time.time() - inicio > timeout:
                    break
                data = audio_q.get()
                if recognizer.AcceptWaveform(data):
                    texto = json.loads(recognizer.Result()).get("text", "")
                    if texto:
                        comando_callback(texto)
                        break
    except Exception as e:
        print(f"Erro em escutar_comando: {e}")

def iniciar_escuta_vosk(callback):
    recognizer = iniciar_modelo()
    if not recognizer:
        return
    escutar_comando(recognizer, callback)

def escutar_loop():
    model_path = "models/vosk-model-small-pt-0.3"
    if not os.path.exists(model_path):
        print("Modelo de voz não encontrado.")
        return

    model = Model(model_path)
    recognizer = KaldiRecognizer(model, 16000)
    recognizer.SetWords(True)
    p = sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                          channels=1)
    with p:
        print("🎙️ Escutando continuamente (loop)...")
        while True:
            data = p.read(4000)[0]
            if recognizer.AcceptWaveform(data):
                texto = json.loads(recognizer.Result()).get("text", "")
                print("🗣️ Texto:", texto)

def escutar_loop_ativado(comando_callback, palavra_ativacao="lili", timeout=10):
    import queue, sounddevice as sd, vosk, json
    q = queue.Queue()
    from vosk import Model, KaldiRecognizer
    modelo = Model("models/vosk-model-small-pt-0.3")
    if not modelo:
        return
    rec = vosk.KaldiRecognizer(modelo, 16000)

    def callback(indata, frames, time, status):
        if status:
            print(status)
        q.put(bytes(indata))

    def escutar():
        try:
            model_path = "models/vosk-model-small-pt-0.3"
            if not os.path.exists(model_path):
                st.session_state["lili_status"] = "❌ Modelo de voz não encontrado."
                return

            model = Model(model_path)
            recognizer = KaldiRecognizer(model, 16000)
            audio_q = queue.Queue()

            def audio_callback(indata, frames, time_info, status):
                if status:
                    print(status)
                audio_q.put(bytes(indata))

            with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                                   channels=1, callback=audio_callback):
                st.session_state["lili_status"] = "🟡 Aguardando palavra de ativação..."
                ativado = False
                ativado_em = 0

                while True:
                    data = audio_q.get()
                    if recognizer.AcceptWaveform(data):
                        texto = json.loads(recognizer.Result()).get("text", "").lower()
                        if texto:
                            st.session_state["lili_status"] = f"🗣️ Você disse: {texto}"

                        if not ativado and palavra_ativacao in texto:
                            st.session_state["lili_status"] = "🔴 Escuta ativa iniciada..."
                            try:
                                tocar_som("bip_on.wav")
                            except:
                                pass
                            ativado = True
                            ativado_em = time.time()
                        elif ativado:
                            if "cancela" in texto or "parar" in texto:
                                st.session_state["lili_status"] = "⛔ Comando cancelado. Retornando à escuta passiva."
                                try:
                                    tocar_som("bip_off.wav")
                                except:
                                    pass
                                ativado = False
                            elif "ajuda" in texto:
                                resposta = "Você pode dizer: gerar laudo, importar paciente, abrir assistente ou cancelar."
                                ler_em_voz_alta(resposta)
                                st.session_state["lili_status"] = f"💬 Lili: {resposta}"
                            elif "repita" in texto:
                                ultimo = st.session_state.get("ultimo_comando_voz", "")
                                if ultimo:
                                    resposta = f"Você disse: {ultimo}"
                                    ler_em_voz_alta(resposta)
                                    st.session_state["lili_status"] = f"🔁 Lili: {resposta}"
                            elif texto.strip():
                                st.session_state["ultimo_comando_voz"] = texto
                                comando_callback(texto)
                                st.session_state["lili_status"] = f"✅ Comando recebido: {texto}"
                                try:
                                    tocar_som("bip_off.wav")
                                except:
                                    pass
                                ativado = False
                            elif time.time() - ativado_em > timeout:
                                st.session_state["lili_status"] = "⌛ Tempo esgotado. Voltando à escuta passiva."
                                try:
                                    tocar_som("bip_off.wav")
                                except:
                                    pass
                                ativado = False
        except Exception as e:
            st.session_state["lili_status"] = f"[ERRO] {e}"

    import threading
    thread = threading.Thread(target=escutar, daemon=True)
    thread.start()

def ouvir_audio_vosk():
    model = Model("models/vosk-model-small-pt-0.3")
    recognizer = KaldiRecognizer(model, 16000)
    recognizer.SetWords(True)
    p = sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                          channels=1)
    texto_final = ""
    with p:
        for _ in range(50):
            data = p.read(4000)[0]
            if recognizer.AcceptWaveform(data):
                texto_final = json.loads(recognizer.Result()).get("text", "").strip()
                if texto_final:
                    break
    return texto_final