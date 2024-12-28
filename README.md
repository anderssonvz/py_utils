# Compressão automatizada com python

Script's para compressão/padronização automática de imagens e musicas com python
O script de compressão de imagens permite a compressão ou conversão de imagens JPG para JPG ou WEBP

O script de imagem foi testado e aparenta ter bom funcionamento!

O script de audio também, entretando após um tempo o script parou, o que acredita ser um erro algo relacionado a máquina e a instalação do FFMPEG no sistema, será testado novamente em breve.

**É recomendado trabalhar com cópias dos seus arquivos originais para evitar problemas que não foram encontrados previamente!**

*Ambos os scripts manipulam todos os arquivos de um diretório e suas subpastas*

## Requisitos para comprimir Imagens

### **Necessário ter o pillow instalado**
    - pip install pillow

## Requisitos para alteração de bitrate de audios
### **Necessário ter o pydub e alguns complementos instalado**
    - pip install pydub mutagen tqdm
* Além disso é preciso instalar o FFMPEG no seu sistema
