from deepgram import (
    DeepgramClient,
    PrerecordedOptions,
    FileSource,
)
from dotenv import load_dotenv
import os

load_dotenv()

deepgram_api = os.getenv("DEEPGRAM_API")

def transcrever_audio(arquivo="../voz.wav"):
    try:
        deepgram = DeepgramClient(deepgram_api)
        with open(arquivo, "rb") as file:
            buffer_data = file.read()
        payload: FileSource = {
            "buffer": buffer_data,
        }
        options: PrerecordedOptions = PrerecordedOptions(
            model="2-general",       
            tier="nova",             
            language="pt",           
            smart_format=True
        )
        response = deepgram.listen.rest.v("1").transcribe_file(payload, options)
        texto = response['results']['channels'][0]['alternatives'][0]['transcript']
        return texto
    except Exception as e:
        print(f"Exception: {e}")