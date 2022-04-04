from typing import Any, Text, Dict, List

from numpy import disp
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from actions.aux_function import AuxFunctions
from actions.video_function import ConverterVideo
from actions.audio_function import ConverterAudio
from test import correction_string

class ConverterMain(Action):
    def name(self) -> Text:
        return "action_converter_main"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        #Track dos slots
        url = tracker.get_slot('url_youtube')
        type_converter_video = tracker.get_slot('type_video')
        type_converter_audio = tracker.get_slot('type_audio')
        #Variaveis
        function_Name = self.run.__name__

        try:
            if type_converter_audio == 'audio' or type_converter_audio == 'Áudio' or type_converter_audio == 'Audio' or type_converter_audio == 'a' or type_converter_audio == 'A':
                url_return, info_audio = self.execute_main('audio', url)
                dispatcher.utter_message(url_return)
            elif type_converter_video == 'video' or type_converter_video == 'Vídeo' or type_converter_video == 'Video' or type_converter_video == 'v' or type_converter_video == 'V':
                url_return, info_video = self.execute_main('video', url)
                dispatcher.utter_message(url_return)
            print('Success in ' + function_Name)
        except:
            print('Error in ' + function_Name)
            return []
        return []

    def execute_main(self, type, url):
        #Variaveis
        function_name = self.execute_main.__name__

        #Objetos
        auxiliar = AuxFunctions()
        video = ConverterVideo()
        audio = ConverterAudio()

        try:
            if type == 'audio':
                video_title, info_Audio = audio.convertAudio(url)
                audio.convertMP4toMP3(video_title)
                audio.uploadAwsMP3(video_title)
                url_return = audio.publicAwsMP3(video_title)
                auxiliar.removeFiles(video_title)
                print('Success in ' + function_name)
                return url_return, info_Audio

            if type == 'video':
                video_title, info_Video = video.convertVideo(url)
                video.uploadAwsMP4(video_title)
                auxiliar.removeFiles(video_title)
                url_return = video.publicAwsMP4(video_title)
                print('Success in ' + function_name)
                return url_return, info_Video

        except:
            print('Error in ' + function_name)
            return None, None
    
    def correction_string(string_type_audio, string_type_video):
        if string_type_audio == None:
            if string_type == 'Vídeo':
                string_type = str(string_type).lower()
                string_type = string_type.replace('í', 'i')
        if string_type_video == None:
            if string_type == "Áudio":
                string_type = str(string_type).lower()
                string_type = string_type.replace('á', 'a')
        if string_type_audio == None and string_type_video == None:
            return None
        return string_type
    
    def description_type(string_type, info_type):
        if string_type:
            if string_type == 'video':
                info_return = 'Nome: ' + info_type['Nome'] + '\n'\
                    + 'Resolução: ' + info_type['Resolução'] + '\n'\
                    + 'Fps: ' + info_type['Fps'] + '\n'\
                    + 'VCodec: ' + info_type['VCodec'] + '\n'\
                    + 'ACodec: ' + info_type['ACodec'] + '\n'\
                    + 'Formato: ' + info_type['Formato'] + '\n\n'\
                    + 'Devido a forma em que o Telegram lida com arquivos, sugiro que baixe o vídeo via link, e salve no diretório desejado!'
            elif string_type == 'audio':
                info_return = 'Nome: ' + info_type['Nome'] + '\n'\
                    + 'Bitrate: ' + info_type['Bitrate'] + '\n'\
                    + 'Codec: ' + info_type['Codec'] + '\n'\
                    + 'Formato: ' + info_type['Formato'] + '\n\n'\
                    + 'Devido a forma em que o Telegram lida com arquivos, sugiro que baixe a música via link, e salve no diretório desejado.'
        return info_return