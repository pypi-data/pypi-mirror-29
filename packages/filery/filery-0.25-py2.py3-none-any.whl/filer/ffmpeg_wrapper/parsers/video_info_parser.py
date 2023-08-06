#!/usr/bin/env python
from marshmallow import Schema
from marshmallow.fields import Int, Nested, Float

from filer.ffmpeg_wrapper.parsers.fields import ASCII


class DispositionParser(Schema):
    attached_pic = Int()
    clean_effects = Int()
    comment = Int()
    default = Int()
    dub = Int()
    forced = Int()
    hearing_impaired = Int()
    karaoke = Int()
    lyrics = Int()
    original = Int()
    visual_impaired = Int()


class StreamParser(Schema):
    avg_frame_rate = ASCII()
    codec_long_name = ASCII()
    codec_name = ASCII()
    codec_tag = ASCII()
    codec_tag_string = ASCII()
    codec_time_base = ASCII()
    codec_type = ASCII()
    coded_height = Int()
    coded_width = Int()
    display_aspect_ratio = ASCII()
    disposition = Nested(DispositionParser)
    duration = Float()
    duration_ts = Int()
    has_b_frames = Int()
    height = Int()
    index = Int()
    level = Int()
    pix_fmt = ASCII()
    r_frame_rate = ASCII()
    refs = Int()
    sample_aspect_ratio = ASCII()
    start_pts = Int()
    start_time = Float()
    time_base = ASCII()
    width = Int()


class TagsParser(Schema):
    comment = ASCII()
    title = ASCII()
    encoder = ASCII()


class FormatParser(Schema):
    filename = ASCII()
    nb_streams = Int()
    nb_programs = Int()
    format_name = ASCII()
    format_long_name = ASCII()
    start_time = Float()
    duration = Float()
    size = Int()
    bit_rate = Int()
    probe_score = Int()
    tags = Nested(TagsParser)


class VideoInfoParser(Schema):
    format = Nested(FormatParser)
    streams = Nested(StreamParser, many=True)





