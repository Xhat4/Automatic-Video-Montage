# Video Processing Project

## Description

This project allows the creation of videos from images with varius effects and transitions applied randomly and automatically. Works with [MoviePy](https://github.com/Zulko/moviepy) library for video edition, custom effects implemented in Python and transitions from [FFmpeg](https://trac.ffmpeg.org/wiki/Xfade).

## Features

- Resizing and adjusting clips based on aspect ratio (if image is vertical creates a background for a 16:9 aspect ratio).
- Application of zoom and scroll effects.
- Automatic transitions between clips.
- Export videos in MP4 format with a specific resolution (1080) and a fixed frame rate (24) that can be changed in the code.

## Requirements

Make sure of install the next libraries before execute the script:

### Python Libraries

- moviepy
- scikit-image
- pillow
- numpy
- ffmpeg-python

Use the next commands to install the libraries:

```bash
pip install moviepy
pip install scikit-image
pip install pillow
pip install numpy
pip install ffmpeg-python
```

## How it works?

After install all the dependencies we have to move the images into the "sources" folder. We should order the images in the folder cause that's the order that the script is gonna follow (example 1.png, 2.jpg, 3.jpg...).
Then execute in the bash the file script.py with the next command:
```bash
python script.py
```
You can change the parameters in the code in order to adjust frame rate, resolution and time for image.

## Project Structure

The project is made up of three files, the main called script.py who resize and adjust clips based on aspect ratio, export the final video and call the other two files. The second is called effectts.py which, as its name indicates, is responsible for applying one of the video effects to each of the clips randomly. And the third, transitions.py, which as its name again expresses, applies one of the transitions loaded from ffmpeg randomly at the end of one clip and the beginning of the next.

Video Example:

https://github.com/Xhat4/Automatic-Video-Montage/assets/40874493/66df622b-8744-429c-a561-761e255aea74

## Contribute!

This project is open source originally written by [Xhat4](https://github.com/Xhat4).

You can contribute by reporting bugs or make new functionalities and send a push request.

## Contact

You can contact me through email: support@elvom.com.
