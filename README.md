# jumpcutter
Automatically edits videos. Explanation here: https://www.youtube.com/watch?v=DQ8orIurGxw

## Some heads-up:

It uses Python 3.

It works on Ubuntu 16.04 and Windows 10. (It might work on other OSs too, we just haven't tested it yet.)

This program relies heavily on ffmpeg. It will start subprocesses that call ffmpeg, so be aware of that!

As the program runs, it saves every frame of the video as an image file in a
temporary folder. If your video is long, this could take a LOT of space.

I have tested:
- A 17-minute video.
- Multiple 2-hour videos. 
  - ***Usage of 64-bit Python is required at this point.***
  - ***A good amount of Memory and a fast SSD is also recomended for decent performance.***


I want to use pyinstaller to turn this into an executable, so non-techy people
can use it EVEN IF they don't have Python and all those libraries. Jabrils 
recommended this to me. However, my pyinstaller build did not work. :( HELP

## Usage

- install all the requirement using by using in the terminal

`pip install -r requirements.txt`

- Using the python file:

`python jumpcutter.py --input_file inputfile.mp4`

The arguments are:

| Command                               | Info                                                                                                                                                                               |
|---------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `--input_file INPUT_FILE`             | The video file you want modified                                                                                                                                                   |
| `--url URL`                           | A video url to download and process through youtube-dl                                                                                                                                             |
| `--output_file OUTPUT_FILE`           | The output file. (optional. if not included, it'll just modify the input file name)                                                                                                |
| `--silent_threshold SILENT_THRESHOLD` | The volume amount that frames' audio needs to surpass to be consider "sounded". It ranges from 0 (silence)to 1 (max volume) (Default: 0.03)                                        |
| `--sounded_speed SOUNDED_SPEED`       | The speed that sounded (spoken) frames should be played at. Typically 1. (Default: 1.00)                                                                                           |
| `--silent_speed SILENT_SPEED`         | The speed that silent frames should be played at. 999999 for jumpcutting. (Default: 5.00)                                                                                          |
| `--frame_margin FRAME_MARGIN`         | Some silent frames adjacent to sounded frames are included to provide context. How many frames on either the side of speech should be included? That's this variable. (Default: 1) |
| `--sample_rate SAMPLE_RATE`           | Sample rate of the input and output videos (Default: 44100)                                                                                                                        |
| `--frame_quality FRAME_QUALITY`       | Quality of frames to be extracted from input video. 1 is highest, 31 is lowest. (Default 3)                                                                                        |


## Building with nix
`nix-build` to get a script with all the libraries and ffmpeg, `nix-build -A bundle` to get a single binary.

## Troubleshooting

- If the video is long you might need a lot of RAM and the x64 version of Python3
- If you have problems installing ffmpeg on Windows follow this link http://blog.gregzaal.com/how-to-install-ffmpeg-on-windows/ (alternative if you are lazy just put the jumpcutter.exe in the same folder)
- try not having spaces in the names of files/folders
- use Python 64 bit.
- update the pytube dependency topytube3
