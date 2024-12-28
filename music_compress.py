import os
import time
from pydub import AudioSegment
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, error
from concurrent.futures import ThreadPoolExecutor, as_completed # Nível de software, uso de múltiplas threads
from tqdm import tqdm  # Para uma barra de progresso visual

def normalize_dir(path):
    path = path.replace('\\','/')
    return path

def process_file(input_file, output_file, target_bitrate):
    input_file = normalize_dir(input_file)
    output_file = normalize_dir(output_file)
    """
    Processa um único arquivo MP3 para verificar e converter o bitrate.
    Preserva metadados e album art.
    """
    try:
        # Verificar bitrate atual
        audio_info = MP3(input_file)
        current_bitrate = int(audio_info.info.bitrate / 1000)  # Convertendo para kbps

        if current_bitrate < target_bitrate:
            return f"Já está abaixo do bitrate desejado: {input_file} ({current_bitrate} kbps)."

        # Carregar o áudio
        audio = AudioSegment.from_file(input_file)
        
        # Preservar metadados
        metadata = None
        try:
            metadata = ID3(input_file)
        except error:
            pass

        # Exportar com novo bitrate
        audio.export(output_file, format="mp3", bitrate=target_bitrate) # ta dando erro aqui, acredito que seja algo relacionado ao FFMPEG no meu pc


        # Reaplicar metadados, se existirem
        if metadata:
            mp3 = MP3(output_file, ID3=ID3)
            mp3.delete()
            for tag in metadata.values():
                mp3.tags.add(tag)
            mp3.save()

        return f"Convertido: {output_file}"
    except Exception as e:
        return f"Erro ao processar {input_file}: {e}"

def convert_bitrate(input_folder, output_folder=None, target_bitrate="128k"):
    """
    Reduz o bitrate de arquivos MP3 mantendo metadados e imagens do álbum, com suporte a paralelização.
    """
    start_time = time.time()  # Marcar o início

    if not output_folder:
        output_folder = input_folder

    # Obter a lista de todos os arquivos MP3
    files_to_process = []
    for root, _, files in os.walk(input_folder):
        for file in files:
            if file.lower().endswith(".mp3"):
                input_file = os.path.join(root, file)
                relative_path = os.path.relpath(root, input_folder)
                output_dir = os.path.join(output_folder, relative_path)
                os.makedirs(output_dir, exist_ok=True)
                output_file = os.path.join(output_dir, file)
                files_to_process.append((input_file, output_file))

    total_files = len(files_to_process)
    print(f"Total de arquivos a serem processados: {total_files}")

    # Processar arquivos em paralelo
    with ThreadPoolExecutor() as executor:
        futures = {
            executor.submit(process_file, input_file, output_file, target_bitrate): (input_file, output_file)
            for input_file, output_file in files_to_process
        }

        with tqdm(total=total_files, desc="Progresso") as pbar:
            for future in as_completed(futures):
                result = future.result()
                print(result)
                pbar.update(1)

    end_time = time.time()  # Marcar o fim
    elapsed_time = end_time - start_time
    print(f"\nTempo total de execução: {elapsed_time:.2f} segundos.")

def main():
    import argparse

    parser = argparse.ArgumentParser(description="Compress mp3 bitrate.")
    parser.add_argument("--input", required=True, help="Input directory containing music files.")
    parser.add_argument("--output", required=True, help="Output directory for compressed musics.")
    parser.add_argument("--bitrate", type=int, default=128, help="set bitrate")

    args = parser.parse_args()

    input_dir = args.input
    output_dir = args.output

    if input_dir == output_dir:
        print("Input and output directories are the same. Files will be overwritten.")
    else:
        os.makedirs(output_dir, exist_ok=True)

    convert_bitrate(
        input_folder = args.input,
        output_folder= args.output,
        target_bitrate = args.bitrate
    )

if __name__ == "__main__":
    main()
