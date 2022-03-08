# import pytube
# import os
# import moviepy.editor as mp
import boto3

# url = "https://www.youtube.com/watch?v=YDDz1Er2IXA"

# video = pytube.YouTube(url)
# video.streams\
#     .filter(progressive=False, file_extension="mp4")\
#     .get_lowest_resolution()\
#     .download(output_path='./download', filename="archive.mp4")

# mp4_file = r'./download/archive.mp4'
# mp3_file = r'./download/audio.mp3'

# clip = mp.VideoFileClip(mp4_file)
# clip.audio.write_audiofile(mp3_file)

def publicAwsMP3():
    url = boto3.client('s3').generate_presigned_url(
        ClientMethod='get_object',
        Params={'Bucket': 'bot-youtube', 'Key': 'audio.mp3'},
        ExpiresIn=3600
    )

    return url

print(publicAwsMP3())