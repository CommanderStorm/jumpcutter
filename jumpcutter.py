import argparse

import process as pro

parser = argparse.ArgumentParser(
    description='Modifies a video file to play at different speeds when there is sound vs. silence.')
parser.add_argument('--input_file', type=str, help='the video file you want modified')
parser.add_argument('--url', type=str, help='A youtube url to download and process')
parser.add_argument('--dir', type=str, help='all .mp4 files in this whole folder will be sequentially jumpcuttet')
parser.add_argument('--output_file', type=str, default="",
                    help="the output file. (optional. if not included, it'll just modify the input file name)")
parser.add_argument('--silent_threshold', type=float, default=0.03,
                    help="the volume amount that frames' audio needs to surpass to be consider \"sounded\". It ranges "
                         "from 0 (silence) to 1 (max volume)")
parser.add_argument('--sounded_speed', type=float, default=1.00,
                    help="the speed that sounded (spoken) frames should be played at. Typically 1.")
parser.add_argument('--silent_speed', type=float, default=5.00,
                    help="the speed that silent frames should be played at. 999999 for jumpcutting.")
parser.add_argument('--frame_margin', type=float, default=1,
                    help="some silent frames adjacent to sounded frames are included to provide context. How many "
                         "frames on either the side of speech should be included? That's this variable.")
parser.add_argument('--sample_rate', type=float, default=44100, help="sample rate of the input and output videos")
parser.add_argument('--frame_rate', type=float, default=30,
                    help="frame rate of the input and output videos. optional... I try to find it out myself, "
                         "but it doesn't always work.")
parser.add_argument('--frame_quality', type=int, default=3,
                    help="quality of frames to be extracted from input video. 1 is highest, 31 is lowest, 3 is the "
                         "default.")

args = parser.parse_args()

frameRate = args.frame_rate
SAMPLE_RATE = args.sample_rate
SILENT_THRESHOLD = args.silent_threshold
FRAME_SPREADAGE = args.frame_margin
NEW_SPEED = [args.silent_speed, args.sounded_speed]
FRAME_QUALITY = args.frame_quality
OUTPUT_FILE = args.output_file

if args.url is not None:
    INPUT_Url = pro.download_file(args.url)
    pro.process_yt(OUTPUT_FILE, SILENT_THRESHOLD, NEW_SPEED, FRAME_SPREADAGE,
                       SAMPLE_RATE, frameRate, FRAME_QUALITY, INPUT_Url)
if args.dir is not None:
    INPUT_Folder = args.dir
    pro.process_folder(OUTPUT_FILE, SILENT_THRESHOLD, NEW_SPEED, FRAME_SPREADAGE,
                       SAMPLE_RATE, frameRate, FRAME_QUALITY, INPUT_Folder)
if args.input_file is not None:
    INPUT_FILE = args.input_file
    pro.process(OUTPUT_FILE, SILENT_THRESHOLD, NEW_SPEED, FRAME_SPREADAGE,
                SAMPLE_RATE, frameRate, FRAME_QUALITY, INPUT_FILE)
