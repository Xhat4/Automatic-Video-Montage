import random
from moviepy.editor import VideoFileClip, CompositeVideoClip, vfx
import os
import subprocess

TEMP_DIR = "temp_clips" #Name of the auxiliary directory for temp files
TRANSITION_DURATION = 1.0  # Total duration of the transition
TARGET_FPS = 24 # Video fps 
OUTPUT_SIZE = (1920, 1080)  # horizontal output 16:9

os.makedirs(TEMP_DIR, exist_ok=True)

# Transitions list
TRANSITIONS = [
    'fade', 'wipeleft', 'wiperight', 'wipeup', 'wipedown', 'slideleft', 'slideright', 'slideup', 
    'slidedown', 'smoothleft', 'smoothright', 'smoothup', 'smoothdown', 'circleclose', 'circleopen', 
    'horzclose', 'horzopen', 'vertclose', 'vertopen', 'diagbl', 'diagbr', 'diagtl', 'diagtr', 'hlslice', 
    'hrslice', 'vuslice', 'vdslice', 'dissolve', 'pixelize', 'radial', 'hblur', 'wipetl', 'wipetr', 
    'wipebl', 'wipebr', 'zoomin', 'hlwind', 'hrwind', 'vuwind', 'vdwind', 'coverleft', 'coverright', 
    'coverup', 'coverdown'
]

def add_background_if_vertical(clip):
    w, h = clip.size
    if h > w:  # Vertical
        # Blurred background effect for vertical videos.
        bg = (
            clip.resize(height=OUTPUT_SIZE[1])
                .fx(vfx.blur, 50)
                .resize(width=OUTPUT_SIZE[0], height=OUTPUT_SIZE[1])
                .set_position("center")
        )

        # Original clip, centered
        scale = OUTPUT_SIZE[1] / h if h < OUTPUT_SIZE[1] else 1
        fg = (
            clip.resize(height=int(h * scale))
                .set_position(("center", "center"))
        )

        return CompositeVideoClip([bg, fg], size=OUTPUT_SIZE) \
            .set_duration(clip.duration) \
            .set_fps(TARGET_FPS)

    else:  # Horizontal
        return clip.resize(width=OUTPUT_SIZE[0]) \
                   .set_position("center") \
                   .set_fps(TARGET_FPS)

def split_head_body_tail(clip_input, target_size=None):
    if isinstance(clip_input, str):
        clip = VideoFileClip(clip_input)
    else:
        clip = clip_input

    clip = add_background_if_vertical(clip)
    duration = clip.duration

    head = clip.subclip(0, min(TRANSITION_DURATION, duration))
    tail = clip.subclip(max(duration - TRANSITION_DURATION, 0), duration)
    body = clip.subclip(min(TRANSITION_DURATION, duration), max(duration - TRANSITION_DURATION, 0))

    return head, body, tail, clip.size

def create_transition(tail_clip, head_clip, index):
    tail_path = os.path.join(TEMP_DIR, f"tail_{index}.mp4")
    head_path = os.path.join(TEMP_DIR, f"head_{index}.mp4")
    transition_path = os.path.join(TEMP_DIR, f"transition_{index}.mp4")

    tail_clip.write_videofile(tail_path, codec="libx264", audio=False, fps=TARGET_FPS)
    head_clip.write_videofile(head_path, codec="libx264", audio=False, fps=TARGET_FPS)

    transition_type = random.choice(TRANSITIONS)

    cmd = [
        "ffmpeg",
        "-i", tail_path,
        "-i", head_path,
        "-filter_complex",
        f"[0:v][1:v]xfade=transition={transition_type}:duration={TRANSITION_DURATION}:offset=0[outv]",
        "-map", "[outv]",
        "-y", "-an",
        transition_path
    ]
    subprocess.run(cmd, check=True)
    return transition_path

def prepare_clips_with_transitions(clips):
    final_clips = []
    prev_tail = None
    target_size = None

    for i, clip in enumerate(clips):
        head, body, tail, clip_size = split_head_body_tail(clip, target_size)
        if not target_size:
            target_size = clip_size

        if prev_tail is not None:
            transition_path = create_transition(prev_tail, head, i)
            final_clips.append(VideoFileClip(transition_path).set_fps(TARGET_FPS).resize(newsize=target_size))

        if body.duration > 0:
            final_clips.append(body.set_fps(TARGET_FPS).resize(newsize=target_size))

        prev_tail = tail

    if prev_tail is not None and prev_tail.duration > 0:
        final_clips.append(prev_tail.set_fps(TARGET_FPS).resize(newsize=target_size))

    return final_clips
