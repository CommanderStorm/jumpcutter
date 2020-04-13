import argparse

import math
import re
import subprocess
from shutil import copyfile, rmtree
import glob
import os
import numpy as np
from audiotsm import phasevocoder
from audiotsm.io.wav import WavReader, WavWriter
from pytube import YouTube
from scipy.io import wavfile
import jumpcutterGui as GUI

TEMP_FOLDER = "TEMP"


def get_max_volume(s):
    max_volume = float(np.max(s))
    min_volume = float(np.min(s))
    return max(max_volume, -min_volume)


def copy_frame(input_frame, output_frame):
    src = TEMP_FOLDER + "/frame{:06d}".format(input_frame + 1) + ".jpg"
    dst = TEMP_FOLDER + "/newFrame{:06d}".format(output_frame + 1) + ".jpg"
    if not os.path.isfile(src):
        return False
    copyfile(src, dst)
    if output_frame % 20 == 19:
        print(str(output_frame + 1) + " time-altered frames saved.")
    return True


def input_to_output_filename(filename):
    dotIndex = filename.rfind(".")
    return filename[:dotIndex] + "_ALTERED" + filename[dotIndex:]


def create_path(file_path):
    # assert (not os.path.exists(file_path)), "The filepath "+file_path+" already exists. Don"t want to overwrite it.
    # Aborting."

    try:
        os.mkdir(file_path)
    except OSError:
        assert False, "Creation of the directory %s failed. (The TEMP folder may already exist. Delete or rename it, " \
                      "and try again.) "


def delete_path(file_path):  # Dangerous! Watch out!
    try:
        rmtree(file_path, ignore_errors=False)
    except OSError:
        print("Deletion of the directory %s failed" % file_path)
        print(OSError)


def download_file(url):
    name = YouTube(url).streams.first().download()
    newname = name.replace(" ", "_")
    os.rename(name, newname)
    return newname


def count_mp4_files_in_folder(input_path: str):
    return len(glob.glob1(input_path, "*.mp4"))


def process(output_file: str, silent_threshold: float, new_speed: list, frame_spreadage: int,
            sample_rate: float, frame_rate: float, frame_quality: int, input_file: str):
    global TEMP_FOLDER
    assert input_file is not None, "why u put no input file, that dum"
    if len(output_file) < 1:
        output_file = input_to_output_filename(input_file)

    # smooth out transitiion"s audio by quickly fading in/out (arbitrary magic number whatever)
    audio_fade_envelope_size = 400
    create_path(TEMP_FOLDER)
    command = "ffmpeg -i " + input_file + " -qscale:v " + str(
        frame_quality) + " " + TEMP_FOLDER + "/frame%06d.jpg -hide_banner"
    subprocess.call(command, shell=True)
    command = "ffmpeg -i " + input_file + " -ab 160k -ac 2 -ar " + str(
        sample_rate) + " -vn " + TEMP_FOLDER + "/audio.wav"
    subprocess.call(command, shell=True)
    command = "ffmpeg -i " + TEMP_FOLDER + "/input.mp4 2>&1"
    with open(TEMP_FOLDER + "/params.txt", "w") as parameter_file:
        subprocess.call(command, shell=True, stdout=parameter_file)
    sample_rate, audio_data = wavfile.read(TEMP_FOLDER + "/audio.wav")
    audio_sample_count = audio_data.shape[0]
    max_audio_volume = get_max_volume(audio_data)
    with open(TEMP_FOLDER + "/params.txt", "r") as parameter_file:
        lines = parameter_file.readlines()
        for line in lines:
            m = re.search("Stream #.*Video.* ([0-9]*) fps", line)
            if m is not None:
                frame_rate = float(m.group(1))
    samples_per_frame = sample_rate / frame_rate
    audio_frame_count: int = int(math.ceil(audio_sample_count / samples_per_frame))
    has_loud_audio = np.zeros(audio_frame_count)

    for audio_frame_iterator in range(audio_frame_count):
        start = int(audio_frame_iterator * samples_per_frame)
        end = min(int((audio_frame_iterator + 1) * samples_per_frame), audio_sample_count)
        audiochunks = audio_data[start:end]
        maxchunks_volume = float(get_max_volume(audiochunks)) / max_audio_volume
        if maxchunks_volume >= silent_threshold:
            has_loud_audio[audio_frame_iterator] = 1
    chunks = [[0, 0, 0]]
    should_include_frame = np.zeros(audio_frame_count)
    for audio_frame_iterator in range(audio_frame_count):
        start = int(max(0, audio_frame_iterator - frame_spreadage))
        end = int(min(audio_frame_count, audio_frame_iterator + 1 + frame_spreadage))
        should_include_frame[audio_frame_iterator] = np.max(has_loud_audio[start:end])
        if audio_frame_iterator >= 1 and should_include_frame[audio_frame_iterator] != should_include_frame[
            audio_frame_iterator - 1]:  # Did we flip?
            chunks.append([chunks[-1][1], audio_frame_iterator, should_include_frame[audio_frame_iterator - 1]])
    chunks.append([chunks[-1][1], audio_frame_count, should_include_frame[audio_frame_iterator - 1]])
    chunks = chunks[1:]
    output_audio_data = np.zeros((0, audio_data.shape[1]))
    output_pointer = 0
    last_existing_frame = None
    for chunk in chunks:
        audio_chunk = audio_data[int(chunk[0] * samples_per_frame):int(chunk[1] * samples_per_frame)]

        s_file = TEMP_FOLDER + "/tempStart.wav"
        e_file = TEMP_FOLDER + "/tempEnd.wav"
        wavfile.write(s_file, sample_rate, audio_chunk)
        with WavReader(s_file) as reader:
            with WavWriter(e_file, reader.channels, reader.samplerate) as writer:
                tsm = phasevocoder(reader.channels, speed=new_speed[int(chunk[2])])
                tsm.run(reader, writer)
        _, altered_audio_data = wavfile.read(e_file)
        leng = altered_audio_data.shape[0]
        end_pointer = output_pointer + leng
        output_audio_data = np.concatenate((output_audio_data, altered_audio_data / max_audio_volume))

        # output_audio_data[output_pointer:end_pointer] = altered_audio_data/max_audio_volume

        # smooth out transitiion"s audio by quickly fading in/out

        if leng < audio_fade_envelope_size:
            output_audio_data[output_pointer:end_pointer] = 0  # audio is less than 0.01 sec, let"s just remove it.
        else:
            premask = np.arange(audio_fade_envelope_size) / audio_fade_envelope_size
            mask = np.repeat(premask[:, np.newaxis], 2, axis=1)  # make the fade-envelope mask stereo
            output_audio_data[output_pointer:output_pointer + audio_fade_envelope_size] *= mask
            output_audio_data[end_pointer - audio_fade_envelope_size:end_pointer] *= 1 - mask

        start_output_frame = int(math.ceil(output_pointer / samples_per_frame))
        end_output_frame = int(math.ceil(end_pointer / samples_per_frame))
        for outputFrame in range(start_output_frame, end_output_frame):
            input_frame = int(chunk[0] + new_speed[int(chunk[2])] * (outputFrame - start_output_frame))
            did_it_work = copy_frame(input_frame, outputFrame)
            if did_it_work:
                last_existing_frame = input_frame
            else:
                copy_frame(last_existing_frame, outputFrame)

        output_pointer = end_pointer
    wavfile.write(TEMP_FOLDER + "/audioNew.wav", sample_rate, output_audio_data)
    """
    outputFrame = math.ceil(output_pointer/samples_per_frame)
    for endGap in range(outputFrame,audio_frame_count):
        copy_frame(int(audio_sample_count/samples_per_frame)-1,endGap)
    """
    command = "ffmpeg " \
              "-framerate {0} " \
              "-i {1}/newFrame%06d.jpg " \
              "-i {2}/audioNew.wav " \
              "-strict -2 {3} " \
              "-thread_queue_size {4}" \
        .format(str(frame_rate), TEMP_FOLDER, TEMP_FOLDER, output_file, os.cpu_count())
    subprocess.call(command, shell=True)
    delete_path(TEMP_FOLDER)


def process_folder(output_file: str, silent_threshold: float, new_speed: list, frame_spreadage: int,
                   sample_rate: int, frame_rate: float, frame_quality: int, input_path: str):
    try:
        number_of_files = count_mp4_files_in_folder(input_path)
    except IOError:
        print("something went wrong when trying to access the '%s' - Folder" % input_path)
        return

    if number_of_files > 0:
        print("\nInput-Source is the '%s' - Folder" % input_path)
        if number_of_files > 1:
            print("('%s' - Folder has %d .mp4 Files)" % (input_path, number_of_files))
        else:
            print("('%s' - Folder has 1 .mp4 File)" % input_path)
        filecount = 1
        for filename in glob.glob1(input_path, "*.mp4"):
            print("\n-----------------------------------------"
                  "\nFile #", filecount)
            filecount += 1
            input_file = input_path + "/" + filename
            process(output_file, silent_threshold, new_speed, frame_spreadage,
                    sample_rate, frame_rate, frame_quality, input_file)
    else:
        print("no .mp4 files found")


def process_yt(output_file: str, silent_threshold: float, new_speed: list, frame_spreadage: int,
               sample_rate: int, frame_rate: float, frame_quality: int, input_url: str):
    downloaded_video = download_file(input_url)
    process(output_file, silent_threshold, new_speed, frame_spreadage,
            sample_rate, frame_rate, frame_quality, downloaded_video)


parser = argparse.ArgumentParser(
    description="Modifies a video file to play at different speeds when there is sound vs. silence.")
parser.add_argument("--input_file", type=str, help="the video file you want modified")
parser.add_argument("--url", type=str, help="A youtube url to download and process")
parser.add_argument("--dir", type=str,
                    help="all .mp4 files in this whole folder will be sequentially processed [to save memory and "
                         "disc space and because it would only run marginally faster if parallel]")
parser.add_argument("--output_file", type=str, default="",
                    help="the output file. (optional. if not included, it'll just modify the input file name)")
parser.add_argument("--silent_threshold", type=float, default=0.03,
                    help="the volume amount that frames' audio needs to surpass to be consider \"sounded\". It ranges "
                         "from 0 (silence) to 1 (max volume)")
parser.add_argument("--sounded_speed", type=float, default=1.00,
                    help="the speed that sounded (spoken) frames should be played at. Typically 1.")
parser.add_argument("--silent_speed", type=float, default=5.00,
                    help="the speed that silent frames should be played at. 999999 for jumpcutting.")
parser.add_argument("--frame_margin", type=int, default=1,
                    help="some silent frames adjacent to sounded frames are included to provide context. How many "
                         "frames on either the side of speech should be included? That's this variable.")
parser.add_argument("--sample_rate", type=int, default=44100, help="sample rate of the input and output videos")
parser.add_argument("--frame_rate", type=float, default=30,
                    help="frame rate of the input and output videos. optional... I try to find it out myself, "
                         "but it doesn't always work.")
parser.add_argument("--frame_quality", type=int, default=3,
                    help="quality of frames to be extracted from input video. 1 is highest, 31 is lowest, 3 is the "
                         "default.")

args = parser.parse_args()

FRAME_RATE = args.frame_rate
SAMPLE_RATE = args.sample_rate
SILENT_THRESHOLD = args.silent_threshold
FRAME_SPREADAGE = args.frame_margin
NEW_SPEED = [args.silent_speed, args.sounded_speed]
FRAME_QUALITY = args.frame_quality
OUTPUT_FILE = args.output_file
GUI_NECESSARY = True

# these if any input option is chosen a gui does not make any sense
if args.url is not None:
    INPUT_URL = args.url
    process_yt(OUTPUT_FILE, SILENT_THRESHOLD, NEW_SPEED, FRAME_SPREADAGE,
               SAMPLE_RATE, FRAME_RATE, FRAME_QUALITY, INPUT_URL)
    GUI_NECESSARY = False
if args.dir is not None:
    INPUT_Folder = args.dir
    process_folder(OUTPUT_FILE, SILENT_THRESHOLD, NEW_SPEED, FRAME_SPREADAGE,
                   SAMPLE_RATE, FRAME_RATE, FRAME_QUALITY, INPUT_Folder)
    GUI_NECESSARY = False
if args.input_file is not None:
    INPUT_FILE = args.input_file
    process(OUTPUT_FILE, SILENT_THRESHOLD, NEW_SPEED, FRAME_SPREADAGE,
            SAMPLE_RATE, FRAME_RATE, FRAME_QUALITY, INPUT_FILE)
    GUI_NECESSARY = False
if GUI_NECESSARY:
    GUI.initiateGUI()
