import os
import glob
import shutil
from Text_to_speech.TTS import Text_to_Speech
from speech_to_text.check_audio import gravar_audio
from speech_to_text.STT import transcrever_audio

def abrir_arquivo(nome_arquivo):
    """Função para abrir um arquivo pelo nome."""
    encontrados = buscar_arquivos(nome_arquivo)
    
    if not encontrados:
        Text_to_Speech(f"Não encontrei nenhum arquivo com o nome {nome_arquivo}")
        return False
    
    if len(encontrados) == 1:
        arquivo = encontrados[0]
        print(f" Abrindo arquivo: {arquivo}")
        os.system(f"xdg-open '{arquivo}' &")  # 'open' no Mac, 'xdg-open' no Linux
        Text_to_Speech(f"Abrindo o arquivo {arquivo}")
        return True
    
    # Se encontrou múltiplos arquivos
    arquivo_escolhido = selecionar_arquivo_com_voz(encontrados)
    
    if arquivo_escolhido:
        print(f"Abrindo arquivo escolhido: {arquivo_escolhido}")
        os.system(f"xdg-open '{arquivo_escolhido}' &")
        Text_to_Speech(f"Abrindo o arquivo {arquivo_escolhido}")
        return True
    else:
        print(f"🛠️ Abrindo primeiro arquivo: {encontrados[0]}")
        os.system(f"xdg-open '{encontrados[0]}' &")
        return True

def buscar_arquivos(nome_arquivo, diretorios=None):
    if diretorios is None:
        diretorios = ["/home/edrio/Documentos", "/home/edrio", "/home/edrio/Documentos/facul", "/home/edrio/Downloads", "/home/edrio/Downloads/books", "/home/edrio/Downloads"]  # padrão

    resultados = []
    for caminho_base in diretorios:
        padrao_busca = f"{caminho_base}/{nome_arquivo}"
        encontrados = glob.glob(padrao_busca, recursive=True)
        resultados.extend(encontrados)

    return resultados

def obter_resposta_audio(opcoes):
    """Função para obter resposta do usuário via áudio usando Deepgram."""
    Text_to_Speech("Por favor, diga o número da opção desejada.")
    
    # Grava a resposta do usuário
    arquivo_audio = "resposta.wav"
    gravar_audio(duracao=3, arquivo=arquivo_audio)
    
    # Transcreve o áudio usando Deepgram
    try:
        texto = transcrever_audio(arquivo_audio)
        print(f"Texto reconhecido: {texto}")
        
        # Tenta extrair um número da resposta
        for palavra in texto.split():
            if palavra.isdigit():
                indice = int(palavra)
                if 1 <= indice <= len(opcoes):
                    return opcoes[indice-1]
        
        # Se falou o nome do arquivo
        for opcao in opcoes:
            nome_opcao = os.path.basename(opcao).lower()
            if nome_opcao in texto.lower():
                return opcao
    except Exception as e:
        print(f"Erro ao reconhecer áudio: {e}")
    
    # Se não conseguiu entender a resposta, retorna None
    return None

def copiar_arquivo(nome_arquivo, destino):
    """Função para copiar um arquivo para um destino específico."""
    encontrados = buscar_arquivos(nome_arquivo)
    
    if not encontrados:
        Text_to_Speech(f"Não encontrei nenhum arquivo com o nome {nome_arquivo}")
        return False
    
    if len(encontrados) == 1:
        return realizar_copia(encontrados[0], destino)
    
    # Se encontrou múltiplos arquivos
    arquivo_escolhido = selecionar_arquivo_com_voz(encontrados)
    if arquivo_escolhido:
        return realizar_copia(arquivo_escolhido, destino)
    
    return False



def realizar_copia(arquivo, destino):
    """Função auxiliar para realizar a cópia de um arquivo."""
    try:
        # Verifica se o destino existe
        if not os.path.exists(destino):
            os.makedirs(destino)
        
        shutil.copy2(arquivo, destino)
        Text_to_Speech(f"Arquivo {arquivo} copiado para {destino}")
        return True
    except Exception as e:
        Text_to_Speech(f"Erro ao copiar arquivo: {e}")
        return False



def mover_arquivo(nome_arquivo, destino):
    """Função para mover um arquivo para um destino específico."""
    encontrados = buscar_arquivos(nome_arquivo)
    
    if not encontrados:
        Text_to_Speech(f"Não encontrei nenhum arquivo com o nome {nome_arquivo}")
        return False
    
    if len(encontrados) == 1:
        return realizar_movimento(encontrados[0], destino)
    
    # Se encontrou múltiplos arquivos
    arquivo_escolhido = selecionar_arquivo_com_voz(encontrados)
    if arquivo_escolhido:
        return realizar_movimento(arquivo_escolhido, destino)
    
    return False

def realizar_movimento(arquivo, destino):
    """Função auxiliar para realizar o movimento de um arquivo."""
    try:
        # Verifica se o destino existe
        if not os.path.exists(destino):
            os.makedirs(destino)
        
        shutil.move(arquivo, destino)
        Text_to_Speech(f"Arquivo {arquivo} movido para {destino}")
        return True
    except Exception as e:
        Text_to_Speech(f"Erro ao mover arquivo: {e}")
        return False

def selecionar_arquivo_com_voz(encontrados):
    """Função para selecionar um arquivo através de comandos de voz."""
    Text_to_Speech(f"Encontrei {len(encontrados)} arquivos. Qual você deseja selecionar?")
    for i, arquivo in enumerate(encontrados, 1):
        nome, extensao = os.path.splitext(os.path.basename(arquivo))
        Text_to_Speech(f"Opção {i}: {nome}, extensão {extensao}")
    
    return obter_resposta_audio(encontrados)



def organizar_arquivos_por_tipo(diretorio="."):
    """Função para organizar arquivos por tipo de extensão."""
    Text_to_Speech("Organizando arquivos por tipo de extensão")
    
    # Define tipos de arquivos comuns
    tipos = {
        "documentos": [".pdf", ".doc", ".docx", ".txt", ".odt"],
        "imagens": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg"],
        "videos": [".mp4", ".mkv", ".avi", ".mov", ".wmv"],
        "audio": [".mp3", ".wav", ".ogg", ".flac", ".aac"],
        "compactados": [".zip", ".rar", ".7z", ".tar", ".gz"],
        "executaveis": [".exe", ".sh", ".bat", ".msi"],
        "codigo": [".py", ".js", ".html", ".css", ".java", ".c", ".cpp"]
    }
    
    # Cria diretórios para cada tipo se não existirem
    for tipo in tipos:
        pasta = os.path.join(diretorio, tipo)
        if not os.path.exists(pasta):
            os.makedirs(pasta)
    
    # Lista todos os arquivos no diretório
    arquivos = [f for f in os.listdir(diretorio) if os.path.isfile(os.path.join(diretorio, f))]
    
    count = 0
    for arquivo in arquivos:
        _, extensao = os.path.splitext(arquivo)
        extensao = extensao.lower()
        
        # Identifica o tipo do arquivo
        for tipo, extensoes in tipos.items():
            if extensao in extensoes:
                origem = os.path.join(diretorio, arquivo)
                destino = os.path.join(diretorio, tipo, arquivo)
                try:
                    shutil.move(origem, destino)
                    count += 1
                except Exception as e:
                    print(f"Erro ao mover {arquivo}: {e}")
                break
    
    Text_to_Speech(f"Organizei {count} arquivos em suas respectivas pastas por tipo")
    return True