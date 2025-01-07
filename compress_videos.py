import os
import subprocess
from concurrent.futures import ThreadPoolExecutor

# Configurações globais de compressão
CODEC = "h264_amf"  # Codec de vídeo para aceleração com GPU AMD (pode ser "hevc_amf" para H.265)
QUALITY = "balanced"  # Qualidade: "speed", "balanced", ou "quality"
OUTPUT_DIR = "compressed_videos"  # Pasta para salvar os vídeos comprimidos

def compress_video_amd(input_path, output_path):
    """
    Função para comprimir um vídeo usando GPU (AMD AMF) com FFmpeg.
    """
    try:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)  # Garante que a pasta de saída exista
        command = [
            "ffmpeg", "-i", input_path,  # Arquivo de entrada
            "-c:v", CODEC,  # Codec de vídeo (AMD AMF)
            #"-quality:v", QUALITY,  # Qualidade do vídeo
            "-b:v", "8M",
            #y"-vf", "scale=iw/2:ih/2", // reduz a resolução
            "-c:a", "copy",  # Mantém o áudio original sem recodificação
            output_path  # Arquivo de saída
        ]
        subprocess.run(command, check=True)  # Executa o comando FFmpeg
        print(f"Comprimido com GPU AMD: {input_path} -> {output_path}")
    except subprocess.CalledProcessError as e:
        print(f"Erro ao comprimir {input_path}: {e}")

def find_videos(folder):
    """
    Retorna uma lista de caminhos de vídeos MP4 na pasta e subpastas.
    """
    videos = []
    for root, _, files in os.walk(folder):
        print(f"PASTA: {root}")
        for file in files:
            print(f"IMAGEM: {file}")
            if file.lower().endswith(".mp4"):  # Filtra apenas arquivos MP4
                videos.append(os.path.join(root, file))
    return videos

def main(input_folder):
    """
    Processa todos os vídeos em uma pasta e subpastas.
    """
    videos = find_videos(input_folder)
    if not videos:
        print("Nenhum vídeo MP4 encontrado na pasta especificada.")
        return

    print(f"Encontrados {len(videos)} vídeos para compressão.")
    
    # Processamento paralelo usando ThreadPoolExecutor
    with ThreadPoolExecutor() as executor:
        for video in videos:
            # Define o caminho de saída
            rel_path = os.path.relpath(video, input_folder)
            output_path = os.path.join(OUTPUT_DIR, rel_path)
            executor.submit(compress_video_amd, video, output_path)

if __name__ == "__main__":
    # Substitua pelo caminho da pasta com os vídeos
    input_folder = "Videos"
    main(input_folder)