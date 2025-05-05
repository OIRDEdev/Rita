import sounddevice as sd
from scipy.io.wavfile import write

def gravar_audio(duracao=5, arquivo="../voz.wav"):
    print("🎙️ Gravando...")
    fs = 44100
    audio = sd.rec(int(duracao * fs), samplerate=fs, channels=1)
    sd.wait()
    write(arquivo, fs, audio)
    print("✅ Gravado.")