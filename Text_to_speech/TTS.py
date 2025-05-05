from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs import play
import os

load_dotenv()

client = ElevenLabs(
  api_key=os.getenv("API_ELEVENLABS"),
)

def Text_to_Speech(texto: str):

    audio = client.text_to_speech.convert(
        text=texto,
        voice_id="deHBYKDC0eGqyeakBFlM",
        model_id="eleven_flash_v2_5",
        output_format="mp3_44100_128",
        language_code="pt"
    )

    play(audio)
