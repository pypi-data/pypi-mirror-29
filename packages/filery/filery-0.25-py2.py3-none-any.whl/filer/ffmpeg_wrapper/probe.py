#!/usr/bin/env python
import subprocess

from filer.ffmpeg_wrapper.utils import is_video

from filer.ffmpeg_wrapper.parsers.video_info_parser import VideoInfoParser

try:
    from subprocess import DEVNULL
except ImportError:
    import os
    DEVNULL = open(os.devnull, 'wb')


def get_video_length(input_video):
    if is_video(input_video):
        info = get_video_info(input_video)
        format_length = info.get('format').get('duration')
        video_stream_length = 0
        audio_stream_length = 0

        for stream in info.get('streams'):
            if stream.get('codec_type') == 'video':
                video_stream_length = stream.get('duration')
            if stream.get('codec_type') == 'audio':
                audio_stream_length = stream.get('duration')

        return dict(
            video_stream_length=video_stream_length,
            audio_stream_length=audio_stream_length,
            format_length=format_length
        )
    else:
        default = float(0)
        return dict(
            video_stream_length=default,
            audio_stream_length=default,
            format_length=default
        )


def get_video_info(input_video):
    if is_video(input_video):

        command_list = ['/usr/bin/ffprobe',
                        '-i',
                        input_video,
                        '-show_format',
                        '-show_streams',
                        '-print_format',
                        'json']

        stdout, stderr = subprocess.Popen(command_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        parser = VideoInfoParser()
        demarshaller = parser.loads(stdout)
        return demarshaller.data
    else:
        default = {}
        return default
