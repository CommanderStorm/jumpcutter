import argparse
import glob
import math
import os
import re
import subprocess
import threading
import time
from shutil import copyfile, rmtree

import numpy as np
from audiotsm import phasevocoder
from audiotsm.io.wav import WavReader, WavWriter
from pytube import YouTube
from scipy.io import wavfile

import jumpcutterGui as Gui

TEMP_FOLDER = "TEMP"
TEMP_TEMP_FOLDER = os.path.join(TEMP_FOLDER, "temp")


#     _____                                                          __      __
#    /     |                                                        /  |    /  |
#    $$$$$ | __    __  _____  ____    ______    _______  __    __  _$$ |_  _$$ |_     ______    ______
#       $$ |/  |  /  |/     \/    \  /      \  /       |/  |  /  |/ $$   |/ $$   |   /      \  /      \
#  __   $$ |$$ |  $$ |$$$$$$ $$$$  |/$$$$$$  |/$$$$$$$/ $$ |  $$ |$$$$$$/ $$$$$$/   /$$$$$$  |/$$$$$$  |
# /  |  $$ |$$ |  $$ |$$ | $$ | $$ |$$ |  $$ |$$ |      $$ |  $$ |  $$ | __ $$ | __ $$    $$ |$$ |  $$/
# $$ \__$$ |$$ \__$$ |$$ | $$ | $$ |$$ |__$$ |$$ \_____ $$ \__$$ |  $$ |/  |$$ |/  |$$$$$$$$/ $$ |
# $$    $$/ $$    $$/ $$ | $$ | $$ |$$    $$/ $$       |$$    $$/   $$  $$/ $$  $$/ $$       |$$ |
#  $$$$$$/   $$$$$$/  $$/  $$/  $$/ $$$$$$$/   $$$$$$$/  $$$$$$/     $$$$/   $$$$/   $$$$$$$/ $$/
#                                   $$ |
#  __  __   ______                  $$ |           __  __
# /  |/  | /      \                 $$/           /  |/  |
# $$ |$$ |/$$$$$$  |  ______    ______    ______  $$ |$$ |
# $$ |$$ |$$ |  $$/  /      \  /      \  /      \ $$ |$$ |
# $$/ $$/ $$ |      /$$$$$$  |/$$$$$$  |/$$$$$$  |$$/ $$/
#         $$ |   __ $$ |  $$ |$$ |  $$/ $$    $$ |
#         $$ \__/  |$$ \__$$ |$$ |      $$$$$$$$/
#         $$    $$/ $$    $$/ $$ |      $$       |
#          $$$$$$/   $$$$$$/  $$/        $$$$$$$/
#   ______    __                 ______    ______
#  /      \  /  |               /      \  /      \
# /$$$$$$  |_$$ |_    __    __ /$$$$$$  |/$$$$$$  |
# $$ \__$$// $$   |  /  |  /  |$$ |_ $$/ $$ |_ $$/
# $$      \$$$$$$/   $$ |  $$ |$$   |    $$   |
#  $$$$$$  | $$ | __ $$ |  $$ |$$$$/     $$$$/
# /  \__$$ | $$ |/  |$$ \__$$ |$$ |      $$ |
# $$    $$/  $$  $$/ $$    $$/ $$ |      $$ |
#  $$$$$$/    $$$$/   $$$$$$/  $$/       $$/
#


def get_max_volume(s):
    max_volume = float(np.max(s))
    min_volume = float(np.min(s))
    return max(max_volume, -min_volume)


def copy_frame(input_frame, output_frame):
    global TEMP_FOLDER, TEMP_TEMP_FOLDER
    src = os.path.join(TEMP_TEMP_FOLDER, "frame{:06d}.jpg".format(input_frame + 1))
    dst = os.path.join(TEMP_FOLDER, "newFrame{:06d}.jpg".format(output_frame + 1))
    if not os.path.isfile(src):
        return False
    copyfile(src, dst)
    if output_frame % 500 == 0:
        print(str(output_frame) + " time-altered frames saved.")
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


def call_subprocess(command: str, shell: bool = False, stdout: str = None):
    timer_start = time.time()
    if stdout is not None:
        with open(stdout, "w+") as parameter_file:
            subprocess.call(command, shell=shell, stdout=parameter_file)
    else:
        subprocess.call(command, shell=shell)
    timer_end = time.time() - timer_start
    print("{}s: {}".format(timer_end, command))


def process(output_file: str, silent_threshold: float, new_speed: list, frame_spreadage: int,
            sample_rate: float, frame_rate: float, frame_quality: int, input_file: str):
    global TEMP_FOLDER, TEMP_TEMP_FOLDER
    assert input_file is not None, "why u put no input file, that dum"
    if len(output_file) < 1:
        output_file = input_to_output_filename(input_file)

    # smooth out transitiion"s audio by quickly fading in/out (arbitrary magic number whatever)
    audio_fade_envelope_size = 400

    create_path(TEMP_FOLDER)
    create_path(TEMP_TEMP_FOLDER)

    command = "ffmpeg -hide_banner -loglevel warning -stats -i " + input_file + " -qscale:v " + str(
        frame_quality) + " " + TEMP_FOLDER + "/temp/frame%06d.jpg"
    picture_seperation_thread = threading.Thread(target=call_subprocess, args=[command])
    picture_seperation_thread.start()
    command = "ffmpeg -hide_banner -loglevel warning -stats -i " + input_file + " -ab 160k -ac 2 -ar " + str(
        sample_rate) + " -vn " + TEMP_FOLDER + "/temp/audio.wav"
    call_subprocess(command, shell=False)
    command = "ffmpeg -hide_banner -loglevel warning -stats -i " + TEMP_FOLDER + "/input.mp4 2>&1"
    call_subprocess(command, shell=False, stdout=os.path.join(TEMP_TEMP_FOLDER, "params.txt"))

    sample_rate, audio_data = wavfile.read(TEMP_FOLDER + "/temp/audio.wav")
    audio_sample_count = audio_data.shape[0]
    max_audio_volume = get_max_volume(audio_data)
    with open(TEMP_FOLDER + "/temp/params.txt", "r") as parameter_file:
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
        if audio_frame_iterator >= 1 and \
                should_include_frame[audio_frame_iterator] != should_include_frame[audio_frame_iterator - 1]:
            # Did we flip?
            chunks.append([chunks[-1][1], audio_frame_iterator, should_include_frame[audio_frame_iterator - 1]])

    chunks.append([chunks[-1][1], audio_frame_count, should_include_frame[audio_frame_iterator - 1]])
    chunks = chunks[1:]

    output_audio_data = np.zeros((0, audio_data.shape[1]))
    output_pointer = 0
    last_existing_frame = None

    print("joining picture_seperation_thread")
    picture_seperation_thread.join()

    timer_start = time.time()
    for chunk in chunks:
        audio_chunk = audio_data[int(chunk[0] * samples_per_frame):int(chunk[1] * samples_per_frame)]

        s_file = TEMP_FOLDER + "/temp/tempStart.wav"
        e_file = TEMP_FOLDER + "/temp/tempEnd.wav"
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
            if copy_frame(input_frame, outputFrame):
                last_existing_frame = input_frame
            else:
                copy_frame(last_existing_frame, outputFrame)

        output_pointer = end_pointer

    timer_end = time.time() - timer_start
    print("Process {} took {} s ".format("chunks", timer_end))

    timerwav = time.time()

    wavfile.write(TEMP_FOLDER + "/audioNew.wav", sample_rate, output_audio_data)
    """
    outputFrame = math.ceil(output_pointer/samples_per_frame)
    for endGap in range(outputFrame,audio_frame_count):
        copy_frame(int(audio_sample_count/samples_per_frame)-1,endGap)
    """
    timer_wav = time.time() - timerwav
    print("Process {} took {} s ".format("wavfile", timer_wav))
    command = "ffmpeg " \
              "-thread_queue_size {0} " \
              "-hide_banner -loglevel warning -stats " \
              "-y " \
              "-framerate {2} " \
              "-i {1}/newFrame%06d.jpg " \
              "-ac 2 " \
              "-i {1}/audioNew.wav " \
              "-framerate {2} " \
              "-c:v libx264 -preset fast -crf 28 -pix_fmt yuvj420p" \
              "{3}" \
        .format(6000, TEMP_FOLDER, str(frame_rate), output_file)

    deletion_thread = threading.Thread(target=delete_path, args=[TEMP_TEMP_FOLDER])
    deletion_thread.start()

    print("\n$> ", command)
    timer_cogent = time.time()

    subprocess.call(command, shell=True)

    timer_cogent = time.time() - timer_cogent
    print("Process {} took {} s "
          "".format("command", timer_cogent))
    delete_path(TEMP_FOLDER)
    deletion_thread.join()


def process_folder(output_dir: str, silent_threshold: float, new_speed: list, frame_spreadage: int,
                   sample_rate: float, frame_rate: float, frame_quality: int, input_path: str):
    try:
        number_of_files = count_mp4_files_in_folder(input_path)
    except IOError:
        print("something went wrong when trying to access the '%s' - Folder" % input_path)
        return

    if number_of_files > 0:
        print("\n\nInput-Source is the '%s' - Folder" % input_path)
        print("This Folder has %d .mp4 Files" % number_of_files)
        filecount = 1
        for filename in glob.glob1(input_path, "*.mp4"):
            print("\n\n----------------------------------------------------------------------------------"
                  "\nFile #{}"
                  "\n\n----------------------------------------------------------------------------------"
                  .format(filecount))
            filecount += 1
            input_file = os.path.join(input_path, filename)
            output_file = input_to_output_filename(os.path.join(output_dir, filename))
            # we are ignoring here that a max filename exists, because I dont think that people would use it that way
            # and if they do .. WHY
            while os.path.isfile(output_file):
                output_file = input_to_output_filename(output_file)
            process(output_file, silent_threshold, new_speed, frame_spreadage,
                    sample_rate, frame_rate, frame_quality, input_file)
    else:
        print("No .mp4 Files found in the Input directory '{}'    :(", input_path)


def process_yt(output_file: str, silent_threshold: float, new_speed: list, frame_spreadage: int,
               sample_rate: float, frame_rate: float, frame_quality: int, input_url: str):
    downloaded_video = download_file(input_url)
    process(output_file, silent_threshold, new_speed, frame_spreadage,
            sample_rate, frame_rate, frame_quality, downloaded_video)


def process_settings(settings: dict):
    combobox = settings["state_of_combobox"]
    new_speed = [settings["silent_speed"], settings["sounded_speed"]]

    if combobox == 0:  # ytdownload
        process_yt("{}".format(settings["destination"]), settings["silent_threshold"], new_speed,
                   settings["frame_margin"], settings["sample_rate"], settings["frame_rate"], settings["frame_quality"],
                   "{}".format(settings["source"]))

    elif combobox == 1:  # folder conversion
        process_folder("{}".format(settings["destination"]), settings["silent_threshold"], new_speed,
                       settings["frame_margin"], settings["sample_rate"], settings["frame_rate"],
                       settings["frame_quality"], "{}".format(settings["source"]))

    else:  # file conversion
        process("{}".format(settings["destination"]), settings["silent_threshold"], new_speed, settings["frame_margin"],
                settings["sample_rate"], settings["frame_rate"], settings["frame_quality"],
                "{}".format(settings["source"]))


#   ______                                                                   __  __  __
#  /      \                                                                 /  |/  |/  |
# /$$$$$$  |  ______   _____  ____   _____  ____    ______   _______    ____$$ |$$ |$$/  _______    ______
# $$ |  $$/  /      \ /     \/    \ /     \/    \  /      \ /       \  /    $$ |$$ |/  |/       \  /      \  ______
# $$ |      /$$$$$$  |$$$$$$ $$$$  |$$$$$$ $$$$  | $$$$$$  |$$$$$$$  |/$$$$$$$ |$$ |$$ |$$$$$$$  |/$$$$$$  |/      |
# $$ |   __ $$ |  $$ |$$ | $$ | $$ |$$ | $$ | $$ | /    $$ |$$ |  $$ |$$ |  $$ |$$ |$$ |$$ |  $$ |$$    $$ |$$$$$$/
# $$ \__/  |$$ \__$$ |$$ | $$ | $$ |$$ | $$ | $$ |/$$$$$$$ |$$ |  $$ |$$ \__$$ |$$ |$$ |$$ |  $$ |$$$$$$$$/
# $$    $$/ $$    $$/ $$ | $$ | $$ |$$ | $$ | $$ |$$    $$ |$$ |  $$ |$$    $$ |$$ |$$ |$$ |  $$ |$$       |
#  $$$$$$/   $$$$$$/  $$/  $$/  $$/ $$/  $$/  $$/  $$$$$$$/ $$/   $$/  $$$$$$$/ $$/ $$/ $$/   $$/  $$$$$$$/
#   ______                                                                     __
#  /      \                                                                   /  |
# /$$$$$$  |  ______    ______   __    __  _____  ____    ______   _______   _$$ |_    _______
# $$ |__$$ | /      \  /      \ /  |  /  |/     \/    \  /      \ /       \ / $$   |  /       |
# $$    $$ |/$$$$$$  |/$$$$$$  |$$ |  $$ |$$$$$$ $$$$  |/$$$$$$  |$$$$$$$  |$$$$$$/  /$$$$$$$/
# $$$$$$$$ |$$ |  $$/ $$ |  $$ |$$ |  $$ |$$ | $$ | $$ |$$    $$ |$$ |  $$ |  $$ | __$$      \
# $$ |  $$ |$$ |      $$ \__$$ |$$ \__$$ |$$ | $$ | $$ |$$$$$$$$/ $$ |  $$ |  $$ |/  |$$$$$$  |
# $$ |  $$ |$$ |      $$    $$ |$$    $$/ $$ | $$ | $$ |$$       |$$ |  $$ |  $$  $$//     $$/
# $$/   $$/ $$/        $$$$$$$ | $$$$$$/  $$/  $$/  $$/  $$$$$$$/ $$/   $$/    $$$$/ $$$$$$$/
#                     /  \__$$ |
#   ______    __      $$    $$/  ______    ______
#  /      \  /  |      $$$$$$/  /      \  /      \
# /$$$$$$  |_$$ |_    __    __ /$$$$$$  |/$$$$$$  |
# $$ \__$$// $$   |  /  |  /  |$$ |_ $$/ $$ |_ $$/
# $$      \$$$$$$/   $$ |  $$ |$$   |    $$   |
#  $$$$$$  | $$ | __ $$ |  $$ |$$$$/     $$$$/
# /  \__$$ | $$ |/  |$$ \__$$ |$$ |      $$ |
# $$    $$/  $$  $$/ $$    $$/ $$ |      $$ |
#  $$$$$$/    $$$$/   $$$$$$/  $$/       $$/
#

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Modifies a video file to play at different speeds when there is sound vs. silence.")
    parser.add_argument("--input_file", type=str, help="the video file you want modified")
    parser.add_argument("--url", type=str, help="A youtube url to download and process")
    parser.add_argument("--input_dir", type=str,
                        help="all .mp4 files in this whole folder will be sequentially processed [to save memory and "
                             "disc space and because it would only run marginally faster if parallel]")
    parser.add_argument("--output_dir", type=str, default=Gui.get_download_folder(),
                        help="While converting a whole Directory using the '--input_dir'-Argument, you can supply a "
                             "Output-Directory in which the Files will be placed")
    parser.add_argument("--output_file", type=str, default="",
                        help="the output file. (optional. if not included, it'll just modify the input file name)")
    parser.add_argument("--silent_threshold", type=float, default=0.03,
                        help="the volume amount that frames' audio needs to surpass to be consider \"sounded\". It "
                             "ranges from 0 (silence) to 1 (max volume)")
    parser.add_argument("--sounded_speed", type=float, default=1.00,
                        help="the speed that sounded (spoken) frames should be played at. Typically 1.")
    parser.add_argument("--silent_speed", type=float, default=5.00,
                        help="the speed that silent frames should be played at. 999999 for jumpcutting.")
    parser.add_argument("--frame_margin", type=int, default=1,
                        help="some silent frames adjacent to sounded frames are included to provide context. How many "
                             "frames on either the side of speech should be included? That's this variable.")
    parser.add_argument("--sample_rate", type=float, default=44100,
                        help="sample rate of the input and output videos")
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
    OUTPUT_DIR = args.output_dir

    GUI_NECESSARY = True

    if args.url is not None:
        INPUT_URL = args.url
        process_yt(OUTPUT_FILE, SILENT_THRESHOLD, NEW_SPEED, FRAME_SPREADAGE,
                   SAMPLE_RATE, FRAME_RATE, FRAME_QUALITY, INPUT_URL)
        GUI_NECESSARY = False
    if args.input_dir is not None:
        INPUT_Folder = args.input_dir
        process_folder(OUTPUT_DIR, SILENT_THRESHOLD, NEW_SPEED, FRAME_SPREADAGE,
                       SAMPLE_RATE, FRAME_RATE, FRAME_QUALITY, INPUT_Folder)
        GUI_NECESSARY = False
    if args.input_file is not None:
        INPUT_FILE = args.input_file
        process(OUTPUT_FILE, SILENT_THRESHOLD, NEW_SPEED, FRAME_SPREADAGE,
                SAMPLE_RATE, FRAME_RATE, FRAME_QUALITY, INPUT_FILE)
        GUI_NECESSARY = False
    # these if any input option is chosen a gui does not make any sense
    if GUI_NECESSARY:
        Gui.initiate_gui()
