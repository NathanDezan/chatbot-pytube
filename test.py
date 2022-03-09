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

# video = pytube.YouTube(url)
# print(video.title)

def convertMP3(url):
    file_archive = 'mp4'
    path_archive = './download/mp3/'
    name_function = convertMP3.__name__
    progressive_filter = 'False'

    try:
        video = pytube.YouTube(url)
        video.streams\
            .filter(progressive=progressive_filter, file_extension=file_archive)\
            .first()\
            .download(output_path=path_archive, filename='teste.mp4')
        print('Success in ' + name_function)
    except:
        print('Error in ' + name_function)
        return None
    return video.title

def remove_Emoji(text):
    name_function = remove_Emoji.__name__

    try:
        emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                        "]+", flags=re.UNICODE)
        print('Success in ' + name_function)

        text_format = emoji_pattern.sub(r'', text)
        text_format = re.sub(' +', ' ', text_format)
    except:
        print('Error in ' + name_function)
        return None
    return text_format

title_video = convertMP3(url5)
print(remove_Emoji(title_video))