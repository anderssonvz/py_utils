# Python Utils

**_É recomendado trabalhar com cópias dos seus arquivos originais para evitar problemas que não foram encontrados previamente, o autor deste diretório não se responsabiliza por qualquer erro ou mal uso dos scripts!_**

Script's feitos para praticidade ao manipular/compactar/renomear arquivos que já me salvaram em algum momento!

*Todos os scripts manipulam todos os arquivos de um diretório e suas subpastas (exceto o de renomear até o momento).*

## _image_compress.py_

Este script é um rework de um script antigo que não paralelizava, portanto é mais eficiente, foi testado e aparenta ter bom funcionamento mas ainda deve ser melhor verificado, permite a compressão ou conversão de imagens JPG para JPG (apenas compactação) ou WEBP (conversão e compactação).

### **Necessário ter o pillow instalado**
    - pip install pillow
    
Executado por linha de comando com:

    python ./image_compress.py --input --output --size-limit --max-width --max-heigth --quality --convert

`--input` - Pasta origin onde o script irá processar.

`--output` - Pasta destino onde os arquivos da pasta origem serão copiados, até o momento o script copia apenas os arquivos processados, logo verifique após a execução!

`--size-limit` - Tamanho limiite (MB) para começar a processar arquivos, caso o arquivo seja menor que este limite o arquivo não será processado.

`--max-width` & `--max-heigth` - Resolução máxima permitida, caso o arquivo seja maior ele redimensiona para a metade da resolução original (Quase isso, precisa ser arrumado pois está redimensionando diretamente). -> Default = '1920' & '1080'.

`--quality` - Qualidade final da compressão do arquivo -> Default = 80.

`--convert` - Conversão do arquivo para WEBP ou apenas a compactação JPG -> Default = 'WBEP'.



## _music_compress.py_
Foi testado e estava em bom funcionamento, após um tempo o script parou, parece ser um erro relacionado a máquina e a instalação do FFMPEG no sistema, será testado novamente em breve.
### **Necessário ter o pydub e alguns complementos instalado**
    - pip install pydub mutagen tqdm
* Além disso é preciso instalar o FFMPEG no seu sistema, verifique como fazer a intalação no seu SO!

Executado por linha de comando com:

    python ./music_compress.py --input --output --bitrate

  `--input` - Pasta origin onde o script irá processar.
  
  `--output` - Pasta destino onde os arquivos da pasta origem serão copiados, até o momento o script copia apenas os arquivos processados, logo verifique após a execução!
  
  `--bitrate` - Bitrate alvo para compactação dos audios, caso o audio tenha o bitrate menor que este parametro ele não será processado!

## _remove_duplicate.py_
Processa um determinado diretório e suas subpastas e manda arquivos duplicados para a lixeira, ao final de execução ele salva um arquivo de log com os itens que foram excluidos!

### Requisitos
Talvez seja necessário ter o módulo send2trash no seu sistema:
    
    -pip install send2trash
    
Executado por linha de comando apenas com o destino do seu diretório após a chamada do script:

    python ./remove_duplicate.py ./meu-diretório

## _remove_prefix.py_
Script simples para remoção de prefixos de arquivos padrão, pode ser alterado para renomear os arquivos, é mais simples trabalha apenas no diretório atual, basta apenas ser executado dentro do diretório!

## A ser feito...

* _Realizar cópias dos arquivos não precessados nos scripts de audio e imagem e testar novamente esses scripts em casos mais específicos com arquivos comrrompidos._

* _Trocar o remove_prefix por um script para renomear arquivos de diretórios e subdiretórios!_
