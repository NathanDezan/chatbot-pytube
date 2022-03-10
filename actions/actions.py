from asyncore import dispatcher_with_send
from cmath import log
from typing import Any, Text, Dict, List
import moviepy.editor as mp
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from pytube import YouTube
import sys
import boto3
import re
import os

class ConverterMain(Action):

    def name(self) -> Text:
        return "action_converter_main"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        resp = ''
        type_converter = ''
        url = tracker.get_slot('url_youtube')
        type_converter_video = tracker.get_slot('type_video')
        type_converter_audio = tracker.get_slot('type_audio')
        resolution = tracker.get_slot('resolutions')

        if type_converter_video == 'video':
            type_converter = 'video'

        if type_converter_audio == 'audio':
            type_converter = 'audio'

        if type_converter_audio != 'audio' and type_converter_video != 'video':
            type_converter = None

        resp, video_title = ConverterMain.execute_main(type_converter, url, resolution)
        dispatcher.utter_message(resp)
        ConverterMain.removeFiles(video_title)

        return []
    
    def execute_main(type, url, quality):

        if type == 'audio':
            video_title = ConverterMain.convertAudio(url)
            ConverterMain.convertMP4toMP3(video_title)
            ConverterMain.uploadAwsMP3(video_title)
            return ConverterMain.publicAwsMP3(video_title), video_title

        if type == 'video':
            video_title = ConverterMain.convertVideo(url, quality)
            ConverterMain.convertMP4toMP3(video_title)
            ConverterMain.createVideo(video_title)
            ConverterMain.uploadAwsMP4(video_title)
            return ConverterMain.publicAwsMP4(video_title), video_title
        
        if type == None:
            return 'Por favor entre com um valor valido!'

    #Funções de conversão de audio
    def convertAudio(url):
        format_archive = 'mp4'
        path_archive = './download/mp3/'
        name_function = ConverterMain.convertAudio.__name__
        progressive_filter = 'False'
        name_archive = ''

        try:
            video = YouTube(url)
            name_archive = ConverterMain.removeEmoji(video.title)
            print(name_archive)
            video.streams\
                .filter(progressive=progressive_filter, file_extension=format_archive)\
                .first()\
                .download(output_path=path_archive, filename=name_archive + '.' + format_archive)
            print('Success in ' + name_function)
        except:
            print('Error in ' + name_function)
            return None
        return name_archive

    def convertMP4toMP3(video_title):
        mp4_file = r'./download/mp3/' + video_title + '.mp4'
        mp3_file = r'./download/mp3/' + video_title + '.mp3'
        function_name = ConverterMain.convertMP4toMP3.__name__
        
        try:
            clip = mp.VideoFileClip(mp4_file)
            clip.audio.write_audiofile(mp3_file)

            print('Success in ' + function_name)
        except:
            print('Error in ' + function_name)

    def uploadAwsMP3(video_title):
        name_function = ConverterMain.uploadAwsMP3.__name__
        name_format = video_title + '.mp3'
        file_name = './download/mp3/' + name_format
        bucket = 'dcbyc'
        object_name = name_format

        s3 = boto3.client('s3')

        try:
            response = s3.upload_file(file_name, bucket, object_name)
            print('Success in ' + name_function)
        except:
            print('Error in ' + name_function)

    def publicAwsMP3(video_title):
        name_format = video_title + '.mp3'
        name_function = ConverterMain.publicAwsMP3.__name__
        bucket = 'dcbyc'
        try:
            url = boto3.client('s3').generate_presigned_url(
                ClientMethod='get_object',
                Params={'Bucket': bucket, 'Key': name_format},
                ExpiresIn=3600
            )
            print('Success in ' + name_function)
        except:
            print('Error in ' + name_function)
            return None
        return url

    #Funções de conversão de video
    def convertVideo(url, quality):
        function_name = ConverterMain.convertVideo.__name__
        file_format_video = 'mp4'
        formatted_name = ''
        path_file_video = './download/mp4/'
        path_file_audio = './download/mp3/'

        try:
            video = YouTube(url)
            formatted_name = ConverterMain.removeEmoji(video.title)
            #Baixa o arquivo em vídeo
            video.streams\
                .filter(progressive=False, file_extension=file_format_video, res=quality)\
                .first()\
                .download(output_path=path_file_video, filename=formatted_name + '.' + file_format_video)
            #Baixa o audio do vídeo
            video.streams\
                .filter(file_extension=file_format_video)\
                .first()\
                .download(output_path=path_file_audio, filename=formatted_name + '.' + file_format_video)
            print('Success in ' + function_name)
        except:
            print('Error in ' + function_name)
        return formatted_name

    def createVideo(video_title):
        path_video = './download/mp4/' + video_title + '.mp4'
        path_audio = './download/mp3/' + video_title + '.mp3'
        function_name = ConverterMain.createVideo.__name__

        try:
            videoclip = mp.VideoFileClip(path_video)
            audio_clip = mp.AudioFileClip(path_audio)
            new_audioclip = mp.CompositeAudioClip([audio_clip])
            videoclip.audio = new_audioclip
            videoclip.write_videofile('./download/' + video_title + '.mp4')
            print('Success in ' + function_name)
        except:
            print('Error in ' + function_name)

    def uploadAwsMP4(video_title):
        file_name = './download/' + video_title + '.mp4'
        bucket = 'dcbyc'
        object_name = video_title + '.mp4'
        function_name = ConverterMain.uploadAwsMP4.__name__

        s3 = boto3.client('s3')

        try:
            response = s3.upload_file(file_name, bucket, object_name)
            print('Success in ' + function_name)
        except:
            print('Error in ' + function_name)

    def publicAwsMP4(video_title):
        function_name = ConverterMain.publicAwsMP4.__name__
        name_format = video_title + '.mp4'
        bucket = 'dcbyc'
        try:
            url = boto3.client('s3').generate_presigned_url(
                ClientMethod='get_object',
                Params={'Bucket': bucket, 'Key': name_format},
                ExpiresIn=3600
            )
            print('Success in ' + function_name)
        except:
            print('Error in ' + function_name)
            return None
        return url
    
    #Funções auxiliares
    def removeEmoji(text):
        name_function = ConverterMain.removeEmoji.__name__

        try:
            emoji_pattern = re.compile("["
            u"\U0001F600-\U0001F64F"  # emoticons
            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
            u"\U0001F680-\U0001F6FF"  # transport & map symbols
            u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                            "]+", flags=re.UNICODE)

            text_format = emoji_pattern.sub(r'', text)
            text_format = re.sub(' +', ' ', text_format)
            text_format = text_format.replace('"', '')
            text_format = text_format.replace('\\', '')
            text_format = text_format.replace('/', '')
            text_format = text_format.replace(':', '')
            text_format = text_format.replace('*', '')
            text_format = text_format.replace('?', '')
            text_format = text_format.replace('<', '')
            text_format = text_format.replace('>', '')
            text_format = text_format.replace('|', '')
            print('Success in ' + name_function)
        except:
            print('Error in ' + name_function)
            return None
        return text_format
    
    def removeFiles(video_title):
        path_video = './download/mp4/' + video_title + '.mp4'
        path_audio = './download/mp3/' + video_title
        path_last_file = './download/' + video_title + '.mp4'
        function_name = ConverterMain.removeFiles.__name__

        try:
            #Remove o arquivo de video no path mp4/
            if os.path.exists(path_video):
                os.remove(path_video)
            
            #Remove o arquivo de audio no path mp3/archive.mp3
            if os.path.exists(path_audio + '.mp3'):
                os.remove(path_audio + '.mp3')
            
            if os.path.exists(path_audio + '.mp4'):
                os.remove(path_audio + '.mp4')
            
            if os.path.exists(path_last_file):
                os.remove(path_last_file)
            
            print('Success in ' + function_name)
        except:
            print('Error in ' + function_name)

class ListResolutions(Action):
  
    def name(self) -> Text:
        return "action_list_resolutions"
  
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        url = tracker.get_slot('url_youtube')

        list_resolutions = ListResolutions.get_resolutions(url)

        dispatcher.utter_message(
            template='utter_resolutions_stream',
            resolutions=list_resolutions
        )
  
        return []
    
    def get_resolutions(url):
        res_exist = {'144p': False, '240p': False, '360p': False, '480p': False, '720p': False, '1080p': False, '1440p': False, '2160p': False, '4320p': False}
        resolutions_list = list()
        function_name = ListResolutions.get_resolutions.__name__

        try:
            video = YouTube(url)
            describe_tube = video.streams.all()

            for i in describe_tube:
                for j in res_exist:
                    res_string = str(i.resolution)
                    if res_string == j:
                        res_exist[j] = True

            for i in res_exist:
                if res_exist[i] == True:
                    resolutions_list.append(i)
            print('Success in ' + function_name)
        except:
            print('Error in ' + function_name)
            return None
        return resolutions_list