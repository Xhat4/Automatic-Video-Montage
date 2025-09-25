import os
from moviepy.editor import *
from moviepy.video import *
from skimage.filters import gaussian
import effects
import transitions
import shutil

# Function to add blur effect to a video
def blur(image):
      return gaussian(image.astype(float), sigma=6)

# Collect all the files names in the resources folder
files = os.listdir("./sources")

# Loop for elements in array files are used to create a clip with a especific duration
#clips = [ImageClip("sources/"+file).set_duration(6)
#      for file in files]

clips = []
for file in os.listdir("./sources"):
    path = os.path.join("sources", file)
    if file.lower().endswith((".jpg", ".jpeg", ".png", ".bmp")):
        clips.append(ImageClip(path).set_duration(6))
    elif file.lower().endswith((".mp4", ".mov", ".avi", ".mkv")):
        clips.append(VideoFileClip(path))

# Create a new array empty for clips with the new size
clipsResized = []

# Loop to detect the aspect ratio from images and create new clips with a new size (1080) and if image is vertical creates a background for a 16:9 aspect ratio
for clip in clips:

      height = clip.h
      width = clip.w

      aspectRatio = round((width / height), 2)

      match aspectRatio:
            case 0.56:
                  print("9:16")
                  clipResized = clip.resize(height=1080)

                  clipCopy = clipResized.set_position((640, 0))
                  leftClip = clipResized.copy().resize(width=840).set_position((0, 0))
                  rightClip = clipResized.copy().resize(width=840).set_position((1247, 0))
                  
                  blurredLeftClip = leftClip.fl_image(blur)
                  blurredRightClip = rightClip.fl_image(blur)

                  clipResized = CompositeVideoClip([blurredLeftClip, blurredRightClip, clipCopy], size=(1920,1080))

            case 0.67:
                  print("2:3")
                  clipResized = clip.resize(height=1080)

                  clipCopy = clipResized.set_position((640, 0))
                  leftClip = clipResized.copy().resize(width=840).set_position((0, 0))
                  rightClip = clipResized.copy().resize(width=840).set_position((1247, 0))
                  
                  blurredLeftClip = leftClip.fl_image(blur)
                  blurredRightClip = rightClip.fl_image(blur)

                  clipResized = CompositeVideoClip([blurredLeftClip, blurredRightClip, clipCopy], size=(1920,1080))

            case 0.75:
                  print("3:4")
                  clipResized = clip.resize(height=1080)

                  clipCopy = clipResized.set_position((640, 0))
                  leftClip = clipResized.copy().resize(width=840).set_position((0, 0))
                  rightClip = clipResized.copy().resize(width=840).set_position((1247, 0))
                  
                  blurredLeftClip = leftClip.fl_image(blur)
                  blurredRightClip = rightClip.fl_image(blur)

                  clipResized = CompositeVideoClip([blurredLeftClip, blurredRightClip, clipCopy], size=(1920,1080))

            case 1.33:
                  print("4:3")
                  cropHeight = int((width / 16) * 9)
                  y_start = int((height - cropHeight) / 2)
                  y_end = y_start + cropHeight
                  clipResized = clip.crop(y1=y_start, y2=y_end).resize(width=1920, height=1080)

            case 1.5:
                  print("3:2")
                  # Crop top and bottom to match 16:9 aspect ratio
                  auxClip = clip.resize(width=1920)
                  crop_height = int((auxClip.w / 16) * 9)
                  y_start = int((auxClip.h - crop_height) / 2)
                  y_end = y_start + crop_height
                  clipResized = auxClip.crop(y1=y_start, y2=y_end)
            
            case 1.78:
                  print("16:9")
                  clipResized = clip.resize(height=1080)

            case 1.77:
                  print("16:9 controlado")
                  clipResized = clip.resize(height=1080)
            case _:
                  print("Aspect ratio not controlled")

      clipsResized.append(effects.randomFunction(clipResized))

# transitions with head, body, tail system. This way video clips can have diferent duration than the clips created with images.
videos = transitions.prepare_clips_with_transitions(clipsResized)

# Concatenate the clips
concatClip = concatenate_videoclips(videos, method="compose")

# Change resolution of final video
finalClip = concatClip.fx(vfx.resize, (1920, 1080))

# Export video
try:
    finalClip.write_videofile("test.mp4", fps=24, audio=False)
finally:
    for clip in videos:
        clip.close()
    shutil.rmtree("temp_clips", ignore_errors=True)
