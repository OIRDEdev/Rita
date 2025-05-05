import comands.comands as comands
import speech_to_text.STT as STT
import speech_to_text.check_audio as check_audio
import conversation.gemini as gemini
import Text_to_speech.TTS as TTS

while True:
    check_audio.gravar_audio()
    texto = STT.transcrever_audio()
    print(f"📝 Texto reconhecido: {texto}")
    if texto:
        executado = comands.interpretar_comando(texto)
        if not executado:
           resposta = gemini.conversar_com_gemini(texto)
           TTS.Text_to_Speech(resposta)
           comands.interpretar_comando(texto)
    else:
        print("😕 Não entendi o que você disse.")
