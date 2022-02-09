# YouPy conversor de vídeo (YouPy conversor of streaming)

## Informações gerais (General Information)
Este projeto é um conversor de vídeo para YouTube. Pode ser utilizado como conversor de vídeo em audio caso necessário. <br>(This project is a video converter for YouTube. It can be used as a video to audio converter if necessary.)

## Tecnologias (Technologies)
* pytube versão: 11.0.1 <br>(pytube version: 11.0.1)

## Como funciona? (How does it work?)
* O programa coleta os parametros via linha de comando. Execute o arquivo "down_tube.py" dentro do diretório raiz do arquivo, da seguinte forma: py .\functions\down_tube.py url type quality format

* Respectivamente: "url" se refere ao link do video no Youtube, "type" é o tipo de conversão solicitada, sendo possível os valores "a" para áudio ou "v" para vídeo, "quality" para a qualidade da conversão, sendo os valores "h" para alta qualidade ou "l" para baixa qualidade, e por fim o paramêtro "format" que possui os formatos "mp4", "avi", "wmv", "flv", "webm", "mov", "mkv", "mpeg".

* Portanto a sintaxe deve ser algo como: py down_tube.py url v h mp4 

* The program collects the parameters via the command line. Run the "down_tube.py" file inside the file's root directory, as follows: py .\functions\down_tube.py url type quality format.

* Respectively: "url" refers to the video link on YouTube, "type" is the requested conversion type, being possible the values ​​"a" for audio or "v" for video, "quality" for the quality of the conversion, being the values ​​"h" for high quality or "l" for low quality, and finally the parameter "format" which has the formats "mp4", "avi", "wmv", "flv", "webm", "mov", "mkv", "mpeg".

* So the syntax should be something like: py down_tube.py url v h mp4