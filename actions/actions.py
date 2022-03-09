from asyncore import dispatcher_with_send
from cmath import log
from typing import Any, Text, Dict, List
import moviepy.editor as mp
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from pytube import YouTube
import sys
import boto3
import re

class ActionIP(Action):

    def name(self) -> Text:
        return "action_ip"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        resp = ""
        url = tracker.get_slot('url_youtube')
        type_converter = tracker.get_slot('type')
        resolution = tracker.get_slot('resolutions')

        resp = ActionIP.execute_main(type_converter, url, resolution)
        dispatcher.utter_message(resp)

        return []
    
    def execute_main(type, url, quality):
        if type == "audio":
            video_title = ActionIP.convertMP3(url)
            ActionIP.convertMP4toMP3(video_title)
            ActionIP.uploadAwsMP3(video_title)
            return ActionIP.publicAwsMP3(video_title)
        
        # if type =="video":
        #     ActionIP.convertStream(url, quality, "mp4")
        #     ActionIP.convertMP4toMP3()
        #     ActionIP.uploadAwsMP4()
        #     return ActionIP.publicAwsMP4()

    def convertMP4toMP3(video_title):
        mp4_file = r'./download/mp3/' + video_title + '.mp4'
        mp3_file = r'./download/mp3/' + video_title + '.mp3'
        function_name = ActionIP.convertMP4toMP3.__name__
        
        try:
            clip = mp.VideoFileClip(mp4_file)
            clip.audio.write_audiofile(mp3_file)

            print('Success in ' + function_name)
        except:
            print('Error in ' + function_name)


    def convertStream(url, quality, format):
        try:
            video = YouTube(url)
            video.streams\
                .filter(progressive=False, file_extension=format, res=quality)\
                .first()\
                .download(output_path='./download/video/')
            audio = video.filter(type = "audio")
            audio\
                .first()\
                .download("./download/audio/")
        except EOFError as error:
            print("Ocorreu um erro!!\n" + error)
        else:
            print("\nDownload finalizado!!")

    def convertMP3(url):
        format_archive = 'mp4'
        path_archive = './download/mp3/'
        name_function = ActionIP.convertMP3.__name__
        progressive_filter = 'False'
        name_archive = ''

        try:
            video = YouTube(url)
            name_archive = ActionIP.remove_Emoji(video.title)
            video.streams\
                .filter(progressive=progressive_filter, file_extension=format_archive)\
                .first()\
                .download(output_path=path_archive, filename=name_archive + '.' + format_archive)
            print('Success in ' + name_function)
        except:
            print('Error in ' + name_function)
            return None
        return name_archive

    def uploadAwsMP4():
        file_name = "./download/archive.mp4"
        bucket = "bot-youtube"
        object_name = "archive.mp4"

        s3 = boto3.client('s3')

        try:
            response = s3.upload_file(file_name, bucket, object_name)
        except:
            print()
        return True

    def uploadAwsMP3(video_title):
        name_function = ActionIP.uploadAwsMP3.__name__
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
        name_function = ActionIP.publicAwsMP3.__name__
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

    def publicAwsMP4():
        url = boto3.client('s3').generate_presigned_url(
            ClientMethod='get_object',
            Params={'Bucket': 'dcbyc', 'Key': 'archive.mp4'},
            ExpiresIn=3600
        )

        return url
    
    def remove_Emoji(text):
        name_function = ActionIP.remove_Emoji.__name__

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
    
class ListUserDetails(Action):
  
    def name(self) -> Text:
        # Name of the action mentioned in the domain.yml file
        return "action_list_user_details"
  
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        url = tracker.get_slot('input_entity')

        list_resolutions = ListUserDetails.get_resolutions(url)

        dispatcher.utter_message(
            template='utter_resolutions_stream',
            resolutions=list_resolutions
        )
  
        return []
    
    def get_resolutions(url):
        video = YouTube(url)
        res_exist = {'144p': False, '240p': False, '360p': False, '480p': False, '720p': False, '1080p': False, '1440p': False, '2160p': False, '4320p': False}
        resolutions_list = list()

        describe_tube = video.streams.all()

        for i in describe_tube:
            for j in res_exist:
                res_string = str(i.resolution)
                if res_string == j:
                    res_exist[j] = True

        for i in res_exist:
            if res_exist[i] == True:
                resolutions_list.append(i)

        return resolutions_list