import os,sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "libraries"))
from moviepy.editor import *
from moviepy.video import *
from skimage.filters import gaussian
import effects
import transitions
import progressBar
import shutil
from tqdm import tqdm
import time
from proglog import ProgressBarLogger
from moviepy.editor import VideoFileClip
import re
import threading
import signal

# Function to add blur effect to a video
def blur(image):
      return gaussian(image.astype(float), sigma=6)

# thread for a loop to control progress bar and execution interruption
stop_thread = False

thread = threading.Thread(target=progressBar.keep_alive, daemon=True)
thread.start()

# capture Ctrl+C to interrupt execution
signal.signal(signal.SIGINT, progressBar.signal_handler)

def natural_sort_key(s):
    # Divide the nae in number and text parts, is used to sort the files 1,2,10...
    return [int(text) if text.isdigit() else text.lower() for text in re.split(r'(\d+)', s)]

# Collect all the files names in the resources folder
files = sorted(os.listdir("./sources"), key=natural_sort_key)

clips = []
for file in files:
    path = os.path.join("sources", file)
    if file.lower().endswith((".jpg", ".jpeg", ".png", ".bmp")):
        clips.append(ImageClip(path).set_duration(6))
    elif file.lower().endswith((".mp4", ".mov", ".avi", ".mkv")):
        clips.append(VideoFileClip(path))

progressBar.update_progresbar(progressBar.progress, 5) #Update the percentage of the video to 5%

# Create a new array empty for clips with the new size
clipsResized = []

# Loop to detect the aspect ratio from images and create new clips with a new size (1080) and if image is vertical creates a background for a 16:9 aspect ratio
for clip in clips:

      height = clip.h
      width = clip.w

      aspectRatio = round((width / height), 2)

      match aspectRatio:
            case 0.56:
                  # print("\n9:16")
                  clipResized = clip.resize(height=1080)

                  clipCopy = clipResized.set_position((640, 0))
                  leftClip = clipResized.copy().resize(width=840).set_position((0, 0))
                  rightClip = clipResized.copy().resize(width=840).set_position((1247, 0))
                  
                  blurredLeftClip = leftClip.fl_image(blur)
                  blurredRightClip = rightClip.fl_image(blur)

                  clipResized = CompositeVideoClip([blurredLeftClip, blurredRightClip, clipCopy], size=(1920,1080))

            case 0.67:
                  # print("\n2:3")
                  clipResized = clip.resize(height=1080)

                  clipCopy = clipResized.set_position((640, 0))
                  leftClip = clipResized.copy().resize(width=840).set_position((0, 0))
                  rightClip = clipResized.copy().resize(width=840).set_position((1247, 0))
                  
                  blurredLeftClip = leftClip.fl_image(blur)
                  blurredRightClip = rightClip.fl_image(blur)

                  clipResized = CompositeVideoClip([blurredLeftClip, blurredRightClip, clipCopy], size=(1920,1080))

            case 0.75:
                  # print("\n3:4")
                  clipResized = clip.resize(height=1080)

                  clipCopy = clipResized.set_position((640, 0))
                  leftClip = clipResized.copy().resize(width=840).set_position((0, 0))
                  rightClip = clipResized.copy().resize(width=840).set_position((1247, 0))
                  
                  blurredLeftClip = leftClip.fl_image(blur)
                  blurredRightClip = rightClip.fl_image(blur)

                  clipResized = CompositeVideoClip([blurredLeftClip, blurredRightClip, clipCopy], size=(1920,1080))

            case 1.33:
                  # print("\n4:3")
                  cropHeight = int((width / 16) * 9)
                  y_start = int((height - cropHeight) / 2)
                  y_end = y_start + cropHeight
                  clipResized = clip.crop(y1=y_start, y2=y_end).resize(width=1920, height=1080)

            case 1.5:
                  # print("\n3:2")
                  # Crop top and bottom to match 16:9 aspect ratio
                  auxClip = clip.resize(width=1920)
                  crop_height = int((auxClip.w / 16) * 9)
                  y_start = int((auxClip.h - crop_height) / 2)
                  y_end = y_start + crop_height
                  clipResized = auxClip.crop(y1=y_start, y2=y_end)
            
            case 1.78:
                  # print("\n16:9")
                  clipResized = clip.resize(height=1080)

            case 1.77:
                  # print("\n16:9 controlado")
                  clipResized = clip.resize(height=1080)
            case _:
                  # print("\nAspect ratio not controlled")

      clipsResized.append(effects.randomFunction(clipResized))

progressBar.update_progresbar(progressBar.progress, 20) #Update the percentage of the video to 20%

# thread to control the progress bar
stop_flag = threading.Event()

thread = threading.Thread(target=progressBar.monitor_temp_clips, args=(stop_flag, files), daemon=True)
thread.start()

# transitions with head, body, tail system. This way video clips can have diferent duration than the clips created with images.
videos = transitions.prepare_clips_with_transitions(clipsResized)

stop_flag.set()
thread.join()

# Concatenate the clips
concatClip = concatenate_videoclips(videos, method="compose")

progressBar.update_progresbar(progressBar.progress, 70) #Update the percentage of the video to 70%

# Change resolution of final video
finalClip = concatClip.fx(vfx.resize, (1920, 1080))

progressBar.update_progresbar(progressBar.progress, 80) #Update the percentage of the video to 80%

# Export video
try:
      finalClip.write_videofile("test.mp4", fps=24, audio=False, logger=progressBar.SimpleLogger(progressBar.update_progresbar)) #logger=None
      progressBar.stop_thread = True
      thread.join()
      time.sleep(2)
      progressBar.update_progresbar(progressBar.progress, 100) # Make sure to update the percentage of the video to 100%
      progressBar.progress.close()
      print("Video finalizado")
finally:
      for clip in videos:
            clip.close()
      shutil.rmtree("temp_clips", ignore_errors=True)
