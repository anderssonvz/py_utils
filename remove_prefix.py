import os
folder = os.getcwd()
prefix = 'abc' # exemplo: remove todos os 'abc' no começo dos arquivos

for file in os.listdir(folder):
    print(f"Original file name: {file}")
    
    old = file.strip()  # remove espaços em branco

    if old.startswith(prefix):
        new = old.replace(prefix, '')
        os.rename(old, new)
        print(f"Renamed {old} to {new}")
    else:
        print(f"No renaming needed for {old}")
