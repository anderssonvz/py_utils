import os
from send2trash import send2trash
import hashlib
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging

def calculate_file_hash(filepath):
    """Calculates the SHA-256 hash of a file."""
    hasher = hashlib.sha256()
    try:
        with open(filepath, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hasher.update(chunk)
        return hasher.hexdigest()
    except Exception as e:
        logging.error(f"Failed to calculate hash for {filepath}: {e}")
        return None

def find_files(directory):
    """Finds all files in a directory and its subdirectories."""
    for root, _, files in os.walk(directory):
        for file in files:
            yield os.path.join(root, file)

def delete_duplicates(directory):
    """Removes duplicate files from the directory and logs the removed files."""
    logging.basicConfig(filename='deleted_files.log', level=logging.INFO, format='%(asctime)s - %(message)s')
    file_hashes = {}
    deleted_files = []

    with ThreadPoolExecutor() as executor:
        futures = {executor.submit(calculate_file_hash, file): file for file in find_files(directory)}

        for future in as_completed(futures):
            file = futures[future]
            file_hash = future.result()

            if file_hash:
                if file_hash in file_hashes:
                    try:
                        #os.remove(file)
                        send2trash(file)
                        deleted_files.append(file)
                        logging.info(f"Deleted: {file}")
                    except Exception as e:
                        logging.error(f"Failed to delete {file}: {e}")
                else:
                    file_hashes[file_hash] = file

    print("Deleted files are logged in 'deleted_files.log'.")
    return deleted_files

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Remove duplicate files from a directory.")
    parser.add_argument('directory', type=str, help="The directory to scan for duplicate files.")
    args = parser.parse_args()

    deleted = delete_duplicates(args.directory)
    print(f"Total files deleted: {len(deleted)}")