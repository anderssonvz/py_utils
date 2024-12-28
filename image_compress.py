#TODO: Verificar resolução // 2 e apenas copiar arquivo quando não necessário processar
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from PIL import Image
import shutil
import logging

def setup_logging(log_file):
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stdout)
        ]
    )

def calculate_space_saved(initial_size, final_size):
    return initial_size - final_size

def resize_image(image, max_width, max_height):
    width, height = image.size
    if width > max_width or height > max_height:
        return image.resize((width // 2, height // 2))
    return image

def convert_image(file_path, output_path, size_limit_mb, max_width, max_height,quality,convert):
    try:
        initial_size = os.path.getsize(file_path) / (1024 * 1024)  # bytes to MB

        if file_path == output_path: return

        # Skip files larger than the limit
        #if initial_size > size_limit_mb:
        #    return None, initial_size, initial_size

        # Open and process the image
        with Image.open(file_path) as img:
            if img.format not in ["JPEG", "JPG"]:
                return None, initial_size, initial_size

            img = resize_image(img, max_width, max_height)
            output_file_path = os.path.join(output_path, os.path.relpath(file_path, start=os.path.dirname(output_path)))
            output_file_path = normalize_dir(output_file_path)
            os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
            output_file_path = output_file_path.replace('.jpg', f'.{convert}') # maybe ?
            output_file_path = output_file_path.replace('.JPG', f'.{convert}')

            if convert.lower() == 'webp': img.save(output_file_path, "WEBP", quality = quality)
            else: img.save(output_file_path, quality = quality) 

            final_size = os.path.getsize(output_file_path) / (1024 * 1024)  # bytes to MB
            return output_file_path, initial_size, final_size
    except Exception as e:
        logging.error(f"Failed to process {file_path}: {e}")
        return None, 0, 0

def normalize_dir(path):
    path = path.replace('\\','/')
    return path

def process_images(input_dir, output_dir, size_limit_mb, max_width, max_height,quality = 80, convert = 'webp'):
    start_time = time.time()
    total_images = 0
    processed_images = 0
    initial_total_size = 0
    final_total_size = 0
    

    with ThreadPoolExecutor() as executor:
        futures = []
        for root, _, files in os.walk(input_dir):
            for file in files:
                if file.lower().endswith(".jpg"):
                    file_path = os.path.join(root, file)
                    normal_file_path = normalize_dir(file_path)
                    futures.append(executor.submit(
                        convert_image,
                        normal_file_path,
                        output_dir,
                        size_limit_mb,
                        max_width,
                        max_height,
                        quality,
                        convert
                    ))

        for future in futures:
            result, initial_size, final_size = future.result()
            total_images += 1
            initial_total_size += initial_size
            final_total_size += final_size
            if result:
                processed_images += 1

    end_time = time.time()
    time_taken = end_time - start_time

    space_saved = calculate_space_saved(initial_total_size, final_total_size)
    logging.info(f"Total Images: {total_images}")
    logging.info(f"Processed Images: {processed_images}")
    logging.info(f"Total Space Saved: {space_saved:.2f} MB")
    logging.info(f"Execution Time: {time_taken:.2f} seconds")
    return total_images, processed_images, space_saved

def main():
    import argparse

    parser = argparse.ArgumentParser(description="Convert JPG images to WEBP format.")
    parser.add_argument("--input", required=True, help="Input directory containing JPG images.")
    parser.add_argument("--output", required=True, help="Output directory for converted images.")
    parser.add_argument("--size-limit", type=float, default=0.5, help="Size limit in MB for image processing.")
    parser.add_argument("--max-width", type=int, default=1920, help="Maximum width of the image.")
    parser.add_argument("--max-height", type=int, default=1080, help="Maximum height of the image.")
    parser.add_argument("--quality", type=int, default=80, help="Maximum quality of the image.")
    parser.add_argument("--convert", type=str, default='webp', help="Format for compress image")

    args = parser.parse_args()

    input_dir = args.input
    output_dir = args.output

    if input_dir == output_dir:
        logging.warning("Input and output directories are the same. Files will be overwritten.")
    else:
        os.makedirs(output_dir, exist_ok=True)

    log_file = os.path.join(output_dir, "conversion.log")
    setup_logging(log_file)

    process_images(
        input_dir,
        output_dir,
        size_limit_mb=args.size_limit,
        max_width=args.max_width,
        max_height=args.max_height,
        quality = args.quality,
        convert = args.convert
    )

if __name__ == "__main__":
    main()

#process_images("./fotos","./teste2",0.1,1280,720,convert='jpg')