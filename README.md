# Video Processing Project

## Description

This project automatically creates videos from images with various visual effects and smooth transitions. Works with [MoviePy](https://github.com/Zulko/moviepy) library for video edition, the custom effects and transitions works with [FFmpeg](https://trac.ffmpeg.org/wiki/Xfade).

## Features

- Resizes and adjusts images to maintain a 16:9 aspect ratio (adds blurred background for vertical images).
- Applies random zoom and scroll effects.
- Automatically adds random transitions between clips.
- Export the final video in MP4 format with a specific resolution (1080) and a fixed frame rate (24) that can be changed in the code.
- Displays a custom progress bar with real-time ETA updates, independent of the MoviePy logger.
- Supports both photos/images and videos of any duration source files
- Number-based ordering for source files in the folder (e.g. 1,2,3,12,13,...)

## Requirements

Make sure of install the next libraries before execute the script:

### Python Libraries

You need to install [FFMPEG](https://www.ffmpeg.org/download.html) from official website

- moviepy
- scikit-image
- pillow
- numpy
- ffmpeg-python
- tqdm

Use the next commands to install the libraries:

```bash
pip install moviepy==1.0.3
pip install scikit-image==0.20.0
pip install pillow==9.5.0
pip install numpy==1.24.2
pip install ffmpeg-python==0.2.0
pip install tqdm==4.64.1
```

Or install all dependencies at once from the local files with:
```bash
pip install -r requirements_local.txt
```

## How it works?

1.  After install all the dependencies we have to move the images and videos into the "sources" folder. 
    The script will process them in alphanumeric order, so name them accordingly (1.jpg, 2.jpg, 3.png,...). 
2.  Then execute in the bash the file script.py with the next command:
```bash
python script.py
```
3.  The program will:
    - Load and adjust all images,
    - Apply random effects and transitions,
    - Render the final video to test.mp4,
    - Show a live progress bar with elapsed and remaining time.
You can change the parameters in the code in order to adjust frame rate, resolution and time for image in transitions.py.

## Project Structure

project/
├── script.py        # Main file: orchestrates the process, renders and exports video
├── effects.py       # Contains all visual effects applied to each clip
├── transitions.py   # Defines the FFmpeg transitions between clips
├── sources/         # Folder containing your input images
└── output/          # (Optional) Folder where the final video is saved

Video Example:

https://github.com/Xhat4/Automatic-Video-Montage/assets/40874493/66df622b-8744-429c-a561-761e255aea74

## Contribute!

This project is open source and was originally created by [Xhat4](https://github.com/Xhat4).

You can contribute by:
- Reporting bugs 
- Suggesting improvements 
- make new code and send a pull request.

## Contact

For questions, suggestions or technical support, reach me at: support@elvom.com.
