import moviepy.editor as mp
from pytube import YouTube
import boto3
from actions.aux_function import AuxFunctions

class ConverterAudio():
    def convertAudio(self, url):
        #Variaveis
        format_archive = '.mp4'
        path_archive = './download/mp3/'
        name_function = self.convertAudio.__name__
        name_archive = ''
        info_Audio = ''
        stream_Audio = ''

        #Objetos
        aux_function = AuxFunctions()

        try:
            video = YouTube(url)
            name_archive = aux_function.removeEmoji(video.title)
            video.streams.order_by('abr').desc().first().download(output_path=path_archive, filename=name_archive + format_archive)
            stream_Audio = video.streams.order_by('abr').desc().first()
            info_Audio = aux_function.information_Audio(stream_Audio, name_archive)

            print('Success in ' + name_function)
        except:
            print('Error in ' + name_function)
            return None, None
        return name_archive, info_Audio

    def convertMP4toMP3(self, video_title):
        #Variaveis utilizadas
        mp4_file = r'./download/mp3/' + video_title + '.mp4'
        mp3_file = r'./download/mp3/' + video_title + '.mp3'
        function_name = self.convertMP4toMP3.__name__
        
        try:
            clip = mp.VideoFileClip(mp4_file)
            clip.audio.write_audiofile(mp3_file)
            print('Success in ' + function_name)
        except:
            print('Error in ' + function_name)

    def uploadAwsMP3(self, video_title):
        #Variaveis
        name_function = self.uploadAwsMP3.__name__
        name_format = video_title + '.mp3'
        file_name = './download/mp3/' + name_format
        bucket = 'dcbyc'
        object_name = name_format

        #Objetos
        s3 = boto3.client('s3')

        try:
            response = s3.upload_file(file_name, bucket, object_name)
            print('Success in ' + name_function)
        except:
            print('Error in ' + name_function)

    def publicAwsMP3(self, video_title):
        #Variaveis
        name_format = video_title + '.mp3'
        name_function = self.publicAwsMP3.__name__
        bucket = 'dcbyc'
        url_return = ''

        try:
            url_return = boto3.client('s3').generate_presigned_url(
                ClientMethod='get_object',
                Params={'Bucket': bucket, 'Key': name_format},
                ExpiresIn=3600
            )
            print('Success in ' + name_function)
        except:
            print('Error in ' + name_function)
            return None
        return url_return