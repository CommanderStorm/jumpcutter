import glob

import jumpcutter as jmp

inputPath = "/Footage/"


def number_of_txt_in_input() -> int:
    return len(glob.glob1(inputPath, "*.mp4"))


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
    print("something went wrong when trying to access the 'TUMSpeak_InputFiles' - Folder")
    txtFiles: int = 0

if txtFiles > 0:
    print("\nInput-Source is the '%s' - Folder" % inputPath)
    if txtFiles > 1:
        print("('TUMSpeak_InputFiles' - Folder has %d .mp4 Files)" % txtFiles)
    else:
        print("('TUMSpeak_InputFiles' - Folder has 1 .mp4 File)")
    filecounter = 1
    for i in glob.glob1(inputPath, "*.mp4"):
        print("\n-----------------------------------------"
              "\nFile #", filecounter)
        filecounter += 1
        INPUT_FILE = inputPath + i
        jmp.process(OUTPUT_FILE, SILENT_THRESHOLD, NEW_SPEED, FRAME_SPREADAGE,
                    SAMPLE_RATE, frameRate, FRAME_QUALITY)

else:
    print("Input-Source is the commandline")
    print("('TUMSpeak_InputFiles' - Folder has %d .txt Files)" % txtFiles)
    text_to_be_converted = input("Please input the Text, you would like to have converted to TUMSpeak\n\t>")
    INPUT_FILE = inputPath + text_to_be_converted
    jmp.process(OUTPUT_FILE, SILENT_THRESHOLD, NEW_SPEED, FRAME_SPREADAGE,
                SAMPLE_RATE, frameRate, FRAME_QUALITY)
