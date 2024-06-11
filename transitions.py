import random
from moviepy.editor import VideoFileClip, concatenate_videoclips, vfx
import os
import subprocess

EFFECT_DURATION = 1
CLIP_DURATION = 6
TRIM_DURATION = CLIP_DURATION / 2  # 2.5 seconds

#transitions

# Function for prepare clips and apply transitions
def prepare_clips_with_transitions(clips):

    # Create a folder called temp_clips for temporal files
    temp_dir = "temp_clips"
    os.makedirs(temp_dir, exist_ok=True)

    # New empty array for clips maded from 2 images with his transition
    videos = []

    # This loop get two clips and make the transition between them
    for i in range(len(clips) - 1):
        clip1_path = os.path.join(temp_dir, f"clip_{i}.mp4")
        clip2_path = os.path.join(temp_dir, f"clip_{i + 1}.mp4")
        output_path = os.path.join(temp_dir, f"transition_{i}.mp4")

        if not os.path.exists(clip1_path):
            clips[i].write_videofile(clip1_path, codec='libx264', fps=24, threads=8)
            
        clips[i + 1].write_videofile(clip2_path, codec='libx264', fps=24, threads=8)

        random_transition(clip1_path, clip2_path, output_path)

        # Add the clip with transition to the empty array created earlier
        videos.append(output_path)

    # Transform the temporal files into VideoClip type objects
    video_clips = convert_temp_clips_to_video_clips(videos)

    # Trim middle clips to avoid loops
    trimmed_clips = trim_intermediate_clips(video_clips, clips)

    return trimmed_clips

# Function to apply a random transition between two clips.
def random_transition(clip1_path, clip2_path, output_path):
    transitions = ['fade', 'wipeleft', 'wiperight', 'wipeup', 'wipedown', 'slideleft', 'slideright', 'slideup', 'slidedown', 'smoothleft', 'smoothright', 'smoothup', 'smoothdown', 'circleclose', 'circleopen', 'horzclose', 'horzopen', 'vertclose', 'vertopen', 'diagbl', 'diagbr', 'diagtl', 'diagtr', 'hlslice', 'hrslice', 'vuslice', 'vdslice', 'dissolve', 'pixelize', 'radial', 'hblur', 'wipetl', 'wipetr', 'wipebl', 'wipebr', 'zoomin', 'hlwind', 'hrwind', 'vuwind', 'vdwind', 'coverleft', 'coverright', 'coverup', 'coverdown']
    selected_transition = random.choice(transitions)
    
    cmd = [
        'ffmpeg', '-i', clip1_path, '-i', clip2_path,
        '-filter_complex', f'[0:v][1:v]xfade=transition={selected_transition}:offset={(CLIP_DURATION - EFFECT_DURATION)}:duration={EFFECT_DURATION}[outv]',
        '-map', '[outv]', '-y', output_path
    ]
    subprocess.run(cmd)

# Function for transform temporal files into VideoClips type objects
def convert_temp_clips_to_video_clips(temp_clip_paths):
    video_clips = []
    for clip_path in temp_clip_paths:
        video_clip = VideoFileClip(clip_path)
        video_clips.append(video_clip)
    return video_clips

# Function to trim middle clips
def trim_intermediate_clips(clips, original_clips):
    trimmed_clips = []

    for i in range(len(clips)):
        if i == 0:
            trimmed_clips.append(clips[i].subclip(0, clips[i].duration - TRIM_DURATION))
        elif i == len(clips) - 1:
            trimmed_clips.append(clips[i].subclip(TRIM_DURATION, clips[i].duration))
        else:
            trimmed_clip = clips[i].subclip(TRIM_DURATION, clips[i].duration - TRIM_DURATION)
            trimmed_clips.append(trimmed_clip)

    return trimmed_clips

# Function to export the final video
def export_final_video(video_clips, output_path):
    final_clip = concatenate_videoclips(video_clips, method="compose")
    final_clip = final_clip.resize((1920, 1080))
    final_clip.write_videofile(output_path, fps=24)

    # Delete temporal files
    for clip in video_clips:
        os.remove(clip.filename)