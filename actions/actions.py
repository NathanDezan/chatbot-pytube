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

class ActionIP(Action):

    def name(self) -> Text:
        return "action_ip"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        type = ""
        resp = ""
        url = tracker.get_slot('input_entity')
        type_video = tracker.get_slot('streaming_type')
        type_audio = tracker.get_slot('audio_type')
        quality = tracker.get_slot('quality_type')

        if type_audio != None:
            type = "audio"

        if type_video != None:
            type = "video"

        resp = ActionIP.execute_main(type, url, quality)
        dispatcher.utter_message(resp)

        return []
    
    def execute_main(type, url, quality):
        if type == "audio":
            ActionIP.optionsStream(url, "audio", quality)
            ActionIP.convertMP4toMP3()
            ActionIP.uploadAwsMP3()
            return ActionIP.publicAwsMP3()
        
        if type =="video":
            ActionIP.optionsStream(url, "video", quality)
            ActionIP.uploadAwsMP4()
            return ActionIP.publicAwsMP4()

    def convertMP4toMP3():
        mp4_file = r'./download/archive.mp4'
        mp3_file = r'./download/audio.mp3'

        clip = mp.VideoFileClip(mp4_file)
        clip.audio.write_audiofile(mp3_file)

    def convertStream(url, quality, format):
        try:
            video = YouTube(url)
            if quality == 'low':
                video.streams\
                    .filter(progressive=False, file_extension=format)\
                    .get_lowest_resolution()\
                    .download(output_path='./download', filename="archive.mp4")
            elif quality == 'high':
                video.streams\
                    .filter(progressive=False, file_extension=format)\
                    .get_highest_resolution()\
                    .download(output_path='./download', filename="archive.mp4")
            else:
                print("Parametro -quality- invalido! Digite (high (alta_qualidade), low (baixa_qualidade))\n")
        except EOFError as erro:
            print("Ocorreu um erro!!\n" + erro)
        else:
            print("\nDownload finalizado!!")

    def convertMP3(url):
        try:
            video = YouTube(url)
            video.streams\
                .filter(progressive=False, file_extension="mp4")\
                .get_lowest_resolution()\
                .download(output_path='./download', filename="archive.mp4")
            print("\nDownload finalizado!")
        except EOFError as erro:
            print("Ocorreu um erro!!\n" + erro)

    def optionsStream(url, type, quality_type):
        if type == "audio":
            ActionIP.convertMP3(url)
        elif type == "video":
            ActionIP.convertStream(url, quality_type, "mp4")
    
    def uploadAwsMP4():
        file_name = "./download/archive.mp4"
        bucket = "bot-youtube"
        object_name = "archive.mp4"

        s3 = boto3.client('s3')

        try:
            response = s3.upload_file(file_name, bucket, object_name)
        except ClientError as e:
            print(e)
            return False
        return True

    def uploadAwsMP3():
        file_name = "./download/audio.mp3"
        bucket = "bot-youtube"
        object_name = "audio.mp3"

        s3 = boto3.client('s3')

        try:
            response = s3.upload_file(file_name, bucket, object_name)
        except ClientError as e:
            print(e)
            return False
        return True

    def publicAwsMP4():
        url = boto3.client('s3').generate_presigned_url(
            ClientMethod='get_object',
            Params={'Bucket': 'bot-youtube', 'Key': 'archive.mp4'},
            ExpiresIn=3600
        )

        return url
    
    def publicAwsMP3():
        url = boto3.client('s3').generate_presigned_url(
            ClientMethod='get_object',
            Params={'Bucket': 'bot-youtube', 'Key': 'audio.mp3'},
            ExpiresIn=3600
        )

        return url