import math
import numpy
from PIL import Image
import random

#effects
def zoom_in_effect(clip, zoom_ratio=0.04):
    def effect(get_frame, t):
            # img variable gets the frame from the clip
            frame = get_frame(t)
            img = Image.fromarray(frame)
            base_size = img.size

            # Calculate the new size of the frame (img.size[0] = width and img.size[1] = height)
            new_size = [
                math.ceil(img.size[0] * (1 + (zoom_ratio * t))),
                math.ceil(img.size[1] * (1 + (zoom_ratio * t)))
            ]

            # The new dimensions must be even.
            new_size[0] = new_size[0] + (new_size[0] % 2)
            new_size[1] = new_size[1] + (new_size[1] % 2)

            img = img.resize(new_size, Image.LANCZOS)

            # Calculate and apply the new dimensions
            x = math.ceil((new_size[0] - base_size[0]) / 2)
            y = math.ceil((new_size[1] - base_size[1]) / 2)

            img = img.crop([
                x, y, new_size[0] - x, new_size[1] - y
            ]).resize(base_size, Image.LANCZOS)

            result = numpy.array(img)
            img.close()

            return result
    return clip.fl(effect)

def zoom_out_effect(clip, zoom_ratio=0.04):
    def effect(get_frame, t):
            # img variable gets the frame from the clip
            frame = get_frame(t)
            img = Image.fromarray(frame)
            base_size = img.size

            # Calculate the new size of the frame (img.size[0] = width and img.size[1] = height)
            # we force the clip to start in a zoomed position to make the zoom out effect adding zoom_ratio * (clip.time)
            new_size = [
                math.ceil(img.size[0] * (1 + (zoom_ratio * clip.duration)  - (zoom_ratio * t))),
                math.ceil(img.size[1] * (1 + (zoom_ratio * clip.duration) - (zoom_ratio * t)))
            ]

            # The new dimensions must be even.
            new_size[0] = new_size[0] - (new_size[0] % 2)
            new_size[1] = new_size[1] - (new_size[1] % 2)

            img = img.resize(new_size, Image.LANCZOS)

            # Calculate the new dimensions to frame after
            x = math.ceil((new_size[0] - base_size[0]) / 2)
            y = math.ceil((new_size[1] - base_size[1]) / 2)

            img = img.crop([
                x, y, new_size[0] - x, new_size[1] - y
            ]).resize(base_size, Image.LANCZOS)

            result = numpy.array(img)
            img.close()

            return result
    return clip.fl(effect)

def scrollDown(clip, y_start=-300, y_end=-320, zoom_ratio=0.25, y_speed=20):
    def effect(get_frame, t):
            # img variable gets the frame from the clip
            frame = get_frame(t)
            img = Image.fromarray(frame)
            base_size = img.size

            # Calculate the new size of the frame
            new_size = [
                math.ceil(img.size[0] * (1 + zoom_ratio)),
                math.ceil(img.size[1] * (1 + zoom_ratio))
            ]

            # The new dimensions must be even.
            new_size[0] -= new_size[0] % 2
            new_size[1] -= new_size[1] % 2

            img = img.resize(new_size, Image.LANCZOS)

            # Calculate the new dimensions to frame after
            x = math.ceil((new_size[0] - base_size[0]) / 2)
            y = math.ceil((new_size[1] - base_size[1]) / 2) + int(y_start + (y_end - y_start) * (t / clip.duration))
            
            # Ensure y does not exceed image boundaries
            y = max(0, min(y, img.size[1] - base_size[1]))

            # Recalculate y for each frame
            y = y + int(t * y_speed)

            img = img.crop([
                x, y, x + base_size[0], y + base_size[1]
            ]).resize(base_size, Image.LANCZOS)

            result = numpy.array(img)
            img.close()

            return result

    return clip.fl(effect)

def scrollUp(clip, y_start=300, y_end=320, zoom_ratio=0.25, y_speed=20):
    def effect(get_frame, t):
            # img variable gets the frame from the clip
            frame = get_frame(t)
            img = Image.fromarray(frame)
            base_size = img.size

            # Calculate the new size of the frame
            new_size = [
                math.ceil(img.size[0] * (1 + zoom_ratio)),
                math.ceil(img.size[1] * (1 + zoom_ratio))
            ]

            # The new dimensions must be even.
            new_size[0] -= new_size[0] % 2
            new_size[1] -= new_size[1] % 2

            # Resize and zoom the image
            img = img.resize(new_size, Image.LANCZOS)

            # Calculate the new dimensions to frame after
            x = math.ceil((new_size[0] - base_size[0]) / 2)
            y = math.ceil((new_size[1] - base_size[1]) / 2) + int(y_start + (y_end - y_start) * (t / clip.duration))
            
            # Ensure does not exceed image boundaries
            y = max(0, min(y, img.size[1] - base_size[1]))

            # Recalculate y for each frame
            y = y - int(t * y_speed)

            img = img.crop([
                x, y, x + base_size[0], y + base_size[1]
            ]).resize(base_size, Image.LANCZOS)

            result = numpy.array(img)
            img.close()

            return result

    return clip.fl(effect)


# Randomize funcions for animations in videos
def randomFunction(clip):
    functions = [zoom_in_effect, zoom_out_effect, scrollDown, scrollUp]
    selectedFunction = random.choice(functions)

    finalClip = selectedFunction(clip)

    return finalClip