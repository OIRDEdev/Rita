import string
import os
import files_managment.files_org as files_org

playlist_path = "/home/edrio/Música/playlist"
comandos = {
        "abra": {
            "navegador": "firefox",
            "spotify": "spotify",
            "terminal": "gnome-terminal",
            "arquivos": "nautilus",
            "calculadora": "gnome-calculator",
            "configurações": "gnome-control-center",
            "editor": "gedit",
            "vscode": "code",
            "vídeo": "vlc",
            "monitor": "gnome-system-monitor",
            "playlist": f"vlc {playlist_path}",
            "youtube": "chromium https://www.youtube.com"
        },
        "feche": {
            "navegador": "pkill firefox",
            "spotify": "pkill spotify",
            "terminal": "pkill gnome-terminal",
            "arquivos": "pkill nautilus",
            "calculadora": "pkill gnome-calculator",
            "configurações": "pkill gnome-control-center",
            "editor": "pkill gedit",
            "vscode": "pkill code",
            "vídeo": "pkill vlc",
            "monitor": "pkill gnome-system-monitor",
            "playlist": "pkill vlc",
            "youtube": "pkill chromium"
        },
        "tocar":{
            "playlist": f"vlc {playlist_path}",
        },

        "procurar": {},
        "abre": {},
        "copia": {},
        "mova": {},
        "mover": {},
        "copiar": {},
        "organizar": {},
    }

def interpretar_comando(text: str):
    Words: list = string_sanitzation(text)

    print(f"Palavras detectadas: {Words}")

    if len(Words) < 2:
        print("Comando muito curto")
        return False
    
    nome, acao, alvo = Verify_comands(Words)
    
    if nome != "rita":
        return False

    response = verificar_comandos(acao, Words)
    
    if not response:
        if acao in comandos and alvo in comandos[acao]:
            comando = comandos[acao][alvo]
            print(f"🛠️ Executando: {comando}")
            os.system(f"{comando} &")
            return True
        else:
            print("Comando não reconhecido")
            return False


def string_sanitzation(text: str):
    text = text.lower().strip()
    text = text.translate(str.maketrans("", "", string.punctuation)) 
    Words_array = text.split()
    return Words_array


def Verify_comands(words: list):
    nome = words[0]
    acao = words[1]
    alvo = words[-1]

    return nome, acao, alvo

def verificar_comandos(acao: str, Words: list):
    # Comandos de arquivo
    if (acao == "abre" or acao == "abra") and "arquivo" in Words:
        try:
            arquivo_idx = Words.index("arquivo")
            if arquivo_idx + 1 < len(Words):
                nome_arquivo = Words[arquivo_idx + 1]
                files_org.abrir_arquivo(nome_arquivo)
                return True
        except ValueError:
            print("Formato de comando inválido")
            return False
    
    # Comando para copiar arquivo
    elif (acao == "copia" or acao == "copiar") and "arquivo" in Words:
        try:
            arquivo_idx = Words.index("arquivo")
            if arquivo_idx + 1 < len(Words) and "para" in Words:
                nome_arquivo = Words[arquivo_idx + 1]
                para_idx = Words.index("para")
                if para_idx + 1 < len(Words):
                    destino = Words[para_idx + 1]
                    files_org.copiar_arquivo(nome_arquivo, destino)
                    return True
        except ValueError:
            print("Formato de comando inválido para copiar")
            return False
    
    # Comando para mover arquivo
    elif (acao == "mova" or acao == "mover") and "arquivo" in Words:
        try:
            arquivo_idx = Words.index("arquivo")
            if arquivo_idx + 1 < len(Words) and "para" in Words:
                nome_arquivo = Words[arquivo_idx + 1]
                para_idx = Words.index("para")
                if para_idx + 1 < len(Words):
                    destino = Words[para_idx + 1]
                    files_org.mover_arquivo(nome_arquivo, destino)
                    return True
        except ValueError:
            print("Formato de comando inválido para mover")
            return False
    
    # Comando para organizar arquivos
    elif acao == "organizar" and "arquivos" in Words:
        diretorio = "."
        try:
            if "em" in Words:
                em_idx = Words.index("em")
                if em_idx + 1 < len(Words):
                    diretorio = Words[em_idx + 1]
            
            files_org.organizar_arquivos_por_tipo(diretorio)
            return True
        except Exception as e:
            print(f"Erro ao organizar arquivos: {e}")
            return False
    
    return False