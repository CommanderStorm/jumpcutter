import glob

import process as pro

inputPath = "/Footage/"


def number_of_txt_in_input() -> int:
    return len(glob.glob1(inputPath, ".mp4"))


frameRate = 30
SAMPLE_RATE = 44100
SILENT_THRESHOLD = 0.0
FRAME_SPREADAGE = 3
NEW_SPEED = [1.25, 7]
INPUT_FILE = ""
FRAME_QUALITY = 2
OUTPUT_FILE = ""

# noinspection PyBroadException
try:
    txtFiles: int = number_of_txt_in_input()
except:
    print("something went wrong when trying to access the '%s' - Folder" % inputPath)
    txtFiles: int = 0

if txtFiles > 0:
    print("\nInput-Source is the '%s' - Folder" % inputPath)
    if txtFiles > 1:
        print("('%s' - Folder has %d .mp4 Files)" % (inputPath, txtFiles))
    else:
        print("('%s' - Folder has 1 .mp4 File)" % inputPath)
    filecount = 1
    for i in glob.glob1(inputPath, ".mp4"):
        print("\n-----------------------------------------"
              "\nFile #", filecount)
        filecount += 1
        INPUT_FILE = inputPath + i
        pro.process(OUTPUT_FILE, SILENT_THRESHOLD, NEW_SPEED, FRAME_SPREADAGE,
                    SAMPLE_RATE, frameRate, FRAME_QUALITY, INPUT_FILE)

else:
    print("Input-Source is the commandline")
    url = input("Please input the URL (for example 'example.mp4')\n\t>")
    INPUT_FILE = pro.download_file(url)
    pro.process(OUTPUT_FILE, SILENT_THRESHOLD, NEW_SPEED, FRAME_SPREADAGE,
                SAMPLE_RATE, frameRate, FRAME_QUALITY, INPUT_FILE)
