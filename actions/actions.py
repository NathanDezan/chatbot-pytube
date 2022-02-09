from asyncore import dispatcher_with_send
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from pytube.cli import download_audio, on_progress
from pytube import YouTube
import sys
import pytube

class ActionIP(Action):

    def name(self) -> Text:
        return "action_ip"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        url = tracker.get_slot('input_entity')
        type = tracker.get_slot('streaming_type')
        quality = tracker.get_slot('quality_type')

        ActionIP.optionsStream(url, type, quality)
        return []
    
    def convertStream(url, quality, format):
        try:
            video = YouTube(url, on_progress_callback=on_progress)
            if quality == 'low':
                video.streams\
                    .filter(file_extension=format)\
                    .get_lowest_resolution()\
                    .download(output_path='./download_video')
            elif quality == 'high':
                video.streams\
                    .filter(file_extension=format)\
                    .get_highest_resolution()\
                    .download(output_path='./download_video')
            else:
                print("Parametro -quality- invalido! Digite (h (alta_qualidade), l (baixa_qualidade))\n")
        except EOFError as erro:
            print("Ocorreu um erro!!\n" + erro)
        else:
            print("\nDownload finalizado!!")

    def convertMP3(url):
        try:
            video = YouTube(url, on_progress_callback=on_progress)
            video.streams\
                .get_audio_only(subtype='mp4')\
                .download(output_path='./download_audio')
        except EOFError as erro:
            print("Ocorreu um erro!!\n" + erro)
        
        else:
            print("\nDownload finalizado!!")

    def optionsStream(url, type, quality_type):
        if(type == "audio"):
            ActionIP.convertMP3(url)
        elif type == "video":
            ActionIP.convertStream(url, quality_type, "mp4")