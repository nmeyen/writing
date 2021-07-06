"""Implements video."""

import logging

from moviepy.editor import concatenate, \
    TextClip, AudioFileClip

from writing.docjson import md_to_docjson
from writing.audio import md_to_audio

log = logging.getLogger('writing.video')
logging.basicConfig(level=logging.INFO)


def _break_text(text):
    words = text.split(' ')
    lines = []
    for word in words:
        if not lines or len(' '.join(lines[-1])) > 50:
            lines.append([])
        lines[-1].append(word)
    return '\n'.join(list(map(
        lambda line: ' '.join(line),
        lines,
    )))


def md_to_video(md_file, video_file=None):
    if video_file is None:
        video_file = md_file.replace('.md', '.mp4')
    audio_file_base = video_file.replace('.mp4', '')
    docjson = md_to_docjson(md_file)
    audio_files = md_to_audio(md_file, audio_file_base)

    frame_clips = []
    for d, audio_file in zip(docjson, audio_files):
        audio_clip = AudioFileClip(audio_file)

        text_clip = TextClip(
            _break_text(d['text']),
            fontsize=32,
            color='black',
            bg_color='white',
            font='Monaco',
            size=(1600, 900),
        ).set_position('center') \
            .set_duration(audio_clip.duration) \
            .set_audio(audio_clip)

        frame_clips.append(text_clip)

    video_clip = concatenate(frame_clips, method='compose')
    video_clip.write_videofile(video_file, fps=5)
    log.info('Wrote %s to %s', md_file, video_file)


if __name__ == '__main__':
    md_to_video(
        'src/writing/assets/test.md',
        '/tmp/test.mp4'
    )
