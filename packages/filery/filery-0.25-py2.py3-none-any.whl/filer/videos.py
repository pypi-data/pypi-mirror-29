from filer.ffmpeg_wrapper.probe import get_video_length, get_video_info
from filer.ffmpeg_wrapper.utils import is_video
from filer.files import File


class VideoFile(File):

    type = 'video'

    @staticmethod
    def is_video(path):
        return is_video(path)

    def length(self, only_format=True):
        if only_format:
            info = self.get_video_length()
            if info.get('format_length'):
                return info.get('format_length')
            else:
                return 0
        else:
            return self.get_video_info()

    def get_video_length(self):
        return get_video_length(self.abspath)

    def get_video_info(self):
        return get_video_info(self.abspath)
