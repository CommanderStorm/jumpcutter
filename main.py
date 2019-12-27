import glob
import os

import process as pro

inputPath = os.path.dirname(__file__) + "/Footage"

frameRate = 30
SAMPLE_RATE = 44100
SILENT_THRESHOLD = 0.1
FRAME_SPREADAGE = 3
NEW_SPEED = [999_999, 1.2]
INPUT_FILE = ""
FRAME_QUALITY = 3
OUTPUT_FILE = ""
number_of_files: int = 0

# noinspection PyBroadException
try:
    number_of_files = len(glob.glob1(inputPath, "*.mp4"))
except:
    print("something went wrong when trying to access the '%s' - Folder" % inputPath)

if number_of_files > 0:
    print("\nInput-Source is the '%s' - Folder" % inputPath)
    if number_of_files > 1:
        print("('%s' - Folder has %d .mp4 Files)" % (inputPath, number_of_files))
    else:
        print("('%s' - Folder has 1 .mp4 File)" % inputPath)
    filecount = 1
    for i in glob.glob1(inputPath, "*.mp4"):
        print("\n-----------------------------------------"
              "\nFile #", filecount)
        filecount += 1
        INPUT_FILE = inputPath + "/" + i
        pro.process(OUTPUT_FILE, SILENT_THRESHOLD, NEW_SPEED, FRAME_SPREADAGE,
                    SAMPLE_RATE, frameRate, FRAME_QUALITY, INPUT_FILE)
else:
    print("Input-Source is the commandline")
    url = input("Please input the URL (for example 'https://www.youtube.com/watch?v=DQ8orIurGxw')\n\t>")
    INPUT_FILE = pro.download_file(url)
    pro.process(OUTPUT_FILE, SILENT_THRESHOLD, NEW_SPEED, FRAME_SPREADAGE,
                SAMPLE_RATE, frameRate, FRAME_QUALITY, INPUT_FILE)
