from pytube import YouTube
import re
import os

#Action
class AuxFunctions():
    def get_resolutions(self, url):
        res_exist = {'144p': False, '240p': False, '360p': False, '480p': False, '720p': False, '1080p': False, '1440p': False, '2160p': False, '4320p': False}
        resolutions_list = list()
        function_name = self.get_resolutions.__name__

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

    def removeEmoji(self, text):
        #Variaveis
        name_function = self.removeEmoji.__name__

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
    
    def removeFiles(self, video_title):
        #Variaveis
        path_video = './download/mp4/' + video_title + '.mp4'
        path_audio = './download/mp3/' + video_title
        path_last_file = './download/' + video_title + '.mp4'
        function_name = self.removeFiles.__name__

        try:
            if os.path.exists(path_video):
                os.remove(path_video)
            
            if os.path.exists(path_audio + '.mp3'):
                os.remove(path_audio + '.mp3')
            
            if os.path.exists(path_audio + '.mp4'):
                os.remove(path_audio + '.mp4')
            
            if os.path.exists(path_last_file):
                os.remove(path_last_file)
            
            print('Success in ' + function_name)
        except:
            print('Error in ' + function_name)
    
    def information_Audio(self, stream, title):
        info_Audio = {'Nome': '', 'Bitrate': '', 'Codec': '', 'Formato': ''}
        function_name = self.information_Audio.__name__

        try:
            info_Audio['Nome'] = title
            info_Audio['Bitrate'] = stream.abr
            info_Audio['Codec'] = stream.codecs[1]
            info_Audio['Formato'] = 'mp3'
            
            print('Success in ' + function_name)
        except:
            print('Error in ' + function_name)
            return None
        return info_Audio

    def information_Video(self, stream, title):
        function_name = self.information_Video.__name__
        info_Video = {'Nome': '', 'Resolução': '', 'Fps': '', 'VCodec': '', 'ACodec': '', 'Formato': ''}
        
        try:
            info_Video['Nome'] = stream.title
            info_Video['Resolução'] = stream.resolution
            info_Video['Fps'] = stream.fps
            info_Video['VCodec'] = stream.codecs[0]
            info_Video['ACodec'] = stream.codecs[1]
            info_Video['Formato'] = 'mp4'
            print('Sucess in ' + function_name)
        except:
            print('Error in ' + function_name)
            return None
        return info_Video