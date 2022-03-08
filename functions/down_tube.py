# from pytube import YouTube
# import sys

# def convertStream(url, quality, format):
#     try:
#         video = YouTube(url)
#         if quality == 'l':
#             video.streams\
#                 .filter(file_extension=format)\
#                 .get_lowest_resolution()\
#                 .download(output_path='./download_video')
#         elif quality == 'h':
#             video.streams\
#                 .filter(file_extension=format)\
#                 .get_highest_resolution()\
#                 .download(output_path='./download_video')
#         else:
#             print("Parametro -quality- invalido! Digite (h (alta_qualidade), l (baixa_qualidade))\n")
#     except EOFError as erro:
#         print("Ocorreu um erro!!\n" + erro)

#     else:
#         print("\nDownload finalizado!!")

# def convertMP3(url):
#     try:
#         video = YouTube(url)
#         video.streams\
#             .get_audio_only(subtype='mp4')\
#             .download(output_path='./download_audio')
#     except EOFError as erro:
#         print("Ocorreu um erro!!\n" + erro)
    
#     else:
#         print("\nDownload finalizado!!")

# def optionsStream():
#     if sys.argv[2] == 'a':
#         convertMP3(sys.argv[1])
#     elif sys.argv[2] == 'v':
#         if sys.argv[4] == 'mp4':
#             convertStream(sys.argv[1], sys.argv[3], sys.argv[4])
#         else:
#             print("Suporte apenas para formato mp4!!\n")
#     else:
#         print("Argumento inválido!! Digite (a (audio), v(video))\n")

# optionsStream()