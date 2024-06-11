import os
from moviepy.editor import *
from moviepy.video import *
from skimage.filters import gaussian
import effects
import transitions
import shutil

# Function to truncate number with only two decimals
def truncate(number, decimals=2):
      return int(number * (10 ** decimals)) / 10 ** decimals

# Function to add blur effect to a video
def blur(image):
      return gaussian(image.astype(float), sigma=6)

# Collect all the files names in the resources folder
files = os.listdir("./sources")

# Loop for elements in array files are used to create a clip with a especific duration
clips = [ImageClip("sources/"+file).set_duration(6)
      for file in files]

# Create a new array empty for clips with the new size
clipsResized = []

# Loop to detect the aspect ratio from images and create new clips with a new size (1080) and if image is vertical creates a background for a 16:9 aspect ratio
for clip in clips:

      height = clip.h
      width = clip.w

      aspectRatio = truncate(width / height)

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

            case 0.66:
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
                  clipResized = auxClip.crop(y1=y_start, y2=y_end) #clip.crop(x1=x_start, x2=x_end, y1=y_start, y2=y_end).resize(width=1920, height=1080)
            
            case 1.77:
                  print("16:9")
                  clipResized = clip.resize(height=1080)


      clipsResized.append(effects.randomFunction(clipResized))

# transitions are added
videos = transitions.prepare_clips_with_transitions(clipsResized)

# Concatenate the clips maded from the images
concatClip = concatenate_videoclips(videos, method="compose")

# Change resolution of final video
finalClip = concatClip.fx(vfx.resize, (1920,1080))

# Export video with a especific name and frame rate
try:
      concatClip.write_videofile("test.mp4", fps=24)

finally:
      # Ensure temporary files are deleted
      for clip in videos:
            clip.close()

      shutil.rmtree("temp_clips")
