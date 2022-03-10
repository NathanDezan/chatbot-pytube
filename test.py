from logging import exception
from pydoc import describe
import pytube
import os
import moviepy.editor as mp
# import boto3
import re

url = "https://www.youtube.com/watch?v=YDDz1Er2IXA"
url2 = 'https://www.youtube.com/watch?v=1La4QzGeaaQ'
url3 = 'https://www.youtube.com/watch?v=Cw_xqTgP_J8'
url4 = 'https://www.youtube.com/watch?v=VAe0WHRgDkM'
url5 = 'https://www.youtube.com/watch?v=W-hcGwW-YYQ'

def convertAudio(url):
    format_archive = 'mp4'
    path_archive = './download/mp3/'
    name_function = convertAudio.__name__
    name_archive = ''

    try:
        video = pytube.YouTube(url)
        name_archive = removeEmoji(video.title)
        print(name_archive)
        video.streams\
            .filter(file_extension=format_archive)\
            .first()\
            .download(output_path=path_archive, filename=name_archive + '.' + format_archive)
        print('Success in ' + name_function)
    except:
        print('Error in ' + name_function)
        return None
    return name_archive

def removeEmoji(text):
    name_function = removeEmoji.__name__

    try:
        emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                        "]+", flags=re.UNICODE)

        text_format = emoji_pattern.sub(r'', text)
        text_format = re.sub(' +', ' ', text_format)
        print('Success in ' + name_function)
    except:
        print('Error in ' + name_function)
        return None
    return text_format

convertAudio(url2)

# video = pytube.YouTube(url)
# print(video.title)

# def convertMP3(url):
#     path_archive = './download/mp4/'
#     name_function = convertMP3.__name__

#     try:
#         video = pytube.YouTube(url)
#         video.streams\
#             .filter(progressive=False, file_extension='mp4', res='2160p')\
#             .first()\
#             .download(output_path=path_archive, filename='url-2160p.mp4')

#         # video.streams\
#         #     .filter(file_extension='mp4')\
#         #     .first()\
#         #     .download(output_path='./download/mp3/', filename='teste.mp4')
#         print('Success in ' + name_function)
#     except:
#         print('Error in ' + name_function)
#         return None
#     return video.title

# def create_Video(video_title):
#     path_video = './download/mp4/' + video_title + '.mp4'
#     path_audio = './download/mp3/' + video_title + '.mp3'
#     videoclip = mp.VideoFileClip(path_video)
#     audio_clip = mp.AudioFileClip(path_audio)
#     # videoclip.set_audio(audio_clip)
#     new_audioclip = mp.CompositeAudioClip([audio_clip])
#     videoclip.audio = new_audioclip
#     videoclip.write_videofile('./download/final_test.mp4')

# def convertMP4toMP3(video_title):
#     mp4_file = r'./download/mp3/' + video_title + '.mp4'
#     mp3_file = r'./download/mp3/' + video_title + '.mp3'
#     function_name = convertMP4toMP3.__name__
#     print(mp4_file, mp3_file)
#     try:
#         clip = mp.VideoFileClip(mp4_file)
#         clip.audio.write_audiofile(mp3_file)

#         print('Success in ' + function_name)
#     except:
#         print('Error in ' + function_name)

# title = convertMP3(url)
# # convertMP4toMP3('teste')
# create_Video('teste')

# def remove_Emoji(text):
#     name_function = remove_Emoji.__name__

#     try:
#         emoji_pattern = re.compile("["
#         u"\U0001F600-\U0001F64F"  # emoticons
#         u"\U0001F300-\U0001F5FF"  # symbols & pictographs
#         u"\U0001F680-\U0001F6FF"  # transport & map symbols
#         u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
#                         "]+", flags=re.UNICODE)
#         print('Success in ' + name_function)

#         text_format = emoji_pattern.sub(r'', text)
#         text_format = re.sub(' +', ' ', text_format)
#     except:
#         print('Error in ' + name_function)
#         return None
#     return text_format

# title_video = convertMP3(url5)
# print(remove_Emoji(title_video))