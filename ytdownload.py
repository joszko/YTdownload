from pytube import YouTube
from pytube import exceptions


def get_stream_info(url, choice_id):
    streams_dict = {}

    try:
        yt = YouTube(url)
        title = yt.title
        if choice_id == 1:
            streams = yt.streams.filter(only_audio=True).all()
            index = 0
            for stream in streams:
                stream_details = f'ITAG: {stream.itag}, Audio Codec: {stream.audio_codec},' \
                                 f'Average Bit Rate: {stream.abr}, ' \
                                 f'File Type: {stream.mime_type.split("/")[1]} '
                streams_dict[index] = stream_details
                index += 0

        elif choice_id == 2:
            streams = yt.streams.filter(only_video=True).all()
            index = 0

            for stream in streams:
                stream_details = f'ITAG: {stream.itag}, Resolution: {stream.resolution}, FPS: {stream.fps}, ' \
                                 f'Video Codec: {stream.video_codec}, ' \
                                 f'File Type: {stream.mime_type.split("/")[1]} '
                streams_dict[index] = stream_details
                index += 1

        elif choice_id == 3:
            streams = yt.streams.filter(progressive=True).all()
            index = 0
            for stream in streams:
                stream_details = f'ITAG: {stream.itag}, Resolution: {stream.resolution}, FPS: {stream.fps}, ' \
                                 f'Video Codec: {stream.video_codec}, Audio Codec: {stream.audio_codec}, ' \
                                 f'File Type: {stream.mime_type.split("/")[1]} '
                streams_dict[index] = stream_details
                index += 1

        result = [streams_dict, title]
        return result

    except exceptions.RegexMatchError:
        print('Wrong link! Link ' + url + 'is not a correct YouTube link!')


def download(url, stream_details):
    youtube = YouTube(url)
    itag = stream_details[stream_details.find(' ') + 1: stream_details.find(',')]
    youtube.streams.get_by_itag(int(itag)).download()


while True:
    while True:
        yt_url = input('Enter the YouTube URL: ')

        print('What do you need? Choose one:')
        print('1: Audio only, \n2: Video only, \n3: Combined (Max Resolution 720p) \n')
        need = input('Enter number: ')

        if int(need) not in (1, 2, 3):
            print('Wrong number!')
            break

        needed_streams = get_stream_info(yt_url, int(need))

        try:
            print('\nMovie Title: ' + needed_streams[1])
        except TypeError:
            break

        print('\nBelow is the list of available streams, please choose the corresponding number:' + '\n')
        print('\n'.join('{}:{}'.format(k, v) for k, v in needed_streams[0].items()))
        choice = input('Which one do you need?: ')

        try:
            chosen = needed_streams[0][int(choice)]
        except KeyError:
            print('Wrong number!')
            break

        download(yt_url, chosen)

        break
