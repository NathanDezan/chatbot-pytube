import moviepy.editor as mp
from pytube import YouTube
import boto3
from actions.aux_function import AuxFunctions

class ConverterVideo():
    def convertVideo(self, url):
        #Variaveis
        function_name = self.convertVideo.__name__
        file_format_video = 'mp4'
        formatted_name = ''
        path_file_video = './download/mp4/'
        info_Video = ''
        stream_Video = ''

        #Objetos
        auxiliar = AuxFunctions()

        try:
            video = YouTube(url)
            formatted_name = auxiliar.removeEmoji(video.title)
            video.streams\
                .filter(file_extension=file_format_video)\
                .first()\
                .download(output_path=path_file_video, filename=formatted_name + '.' + file_format_video)

            stream_Video = video.streams.first()
            info_Video = auxiliar.information_Video(stream_Video, formatted_name)

            print('Success in ' + function_name)
        except:
            print('Error in ' + function_name)
            return None, None
        return formatted_name, info_Video

    def createVideo(self, video_title):
        path_video = './download/mp4/' + video_title + '.mp4'
        path_audio = './download/mp3/' + video_title + '.mp3'
        function_name = self.createVideo.__name__

        try:
            videoclip = mp.VideoFileClip(path_video)
            audio_clip = mp.AudioFileClip(path_audio)
            new_audioclip = mp.CompositeAudioClip([audio_clip])
            videoclip.audio = new_audioclip
            videoclip.write_videofile('./download/' + video_title + '.mp4')
            print('Success in ' + function_name)
        except:
            print('Error in ' + function_name)
            return False
        return True

    def uploadAwsMP4(self, video_title):
        file_name = './download/mp4/' + video_title + '.mp4'

        bucket = 'dcbyc'
        object_name = video_title + '.mp4'
        function_name = self.uploadAwsMP4.__name__

        s3 = boto3.client('s3')

        try:
            response = s3.upload_file(file_name, bucket, object_name)
            print('Success in ' + function_name)
        except:
            print('Error in ' + function_name)

    def publicAwsMP4(self, video_title):
        #Variaveis
        function_name = self.publicAwsMP4.__name__
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