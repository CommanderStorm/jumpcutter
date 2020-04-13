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
    # assert (not os.path.exists(file_path)), "The filepath "+file_path+" already exists. Don't want to overwrite it.
    # Aborting."

    try:
        os.mkdir(file_path)
    except OSError:
        assert False, "Creation of the directory %s failed. (The TEMP folder may already exist. Delete or rename it, " \
                      "and try again.) "


def deletePath(file_path):  # Dangerous! Watch out!
    try:
        rmtree(file_path, ignore_errors=False)
    except OSError:
        print("Deletion of the directory %s failed" % file_path)
        print(OSError)


def download_file(url):
    name = YouTube(url).streams.first().download()
    newname = name.replace(' ', '_')
    os.rename(name, newname)
    return newname


def process(output_file: str, silent_threshold: float, new_speed: list, frame_spreadage: float,
            sample_rate: float, frame_rate: float, frame_quality: int, input_file: str):
    global TEMP_FOLDER
    assert input_file is not None, "why u put no input file, that dum"
    if len(output_file) < 1:
        output_file = input_to_output_filename(input_file)

    # smooth out transitiion's audio by quickly fading in/out (arbitrary magic number whatever)
    AUDIO_FADE_ENVELOPE_SIZE = 400
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
    sampleRate, audioData = wavfile.read(TEMP_FOLDER + "/audio.wav")
    audioSampleCount = audioData.shape[0]
    maxAudioVolume = get_max_volume(audioData)
    with open(TEMP_FOLDER + "/params.txt", 'r') as parameter_file:
        lines = parameter_file.readlines()
        for line in lines:
            m = re.search('Stream #.*Video.* ([0-9]*) fps', line)
            if m is not None:
                frame_rate = float(m.group(1))
    samples_per_frame = sampleRate / frame_rate
    audio_frame_count: int = int(math.ceil(audioSampleCount / samples_per_frame))
    has_loud_audio = np.zeros(audio_frame_count)
    i: int
    for i in range(audio_frame_count):
        start = int(i * samples_per_frame)
        end = min(int((i + 1) * samples_per_frame), audioSampleCount)
        audiochunks = audioData[start:end]
        maxchunks_volume = float(get_max_volume(audiochunks)) / maxAudioVolume
        if maxchunks_volume >= silent_threshold:
            has_loud_audio[i] = 1
    chunks = [[0, 0, 0]]
    should_include_frame = np.zeros(audio_frame_count)
    for i in range(audio_frame_count):
        start = int(max(0, i - frame_spreadage))
        end = int(min(audio_frame_count, i + 1 + frame_spreadage))
        should_include_frame[i] = np.max(has_loud_audio[start:end])
        if i >= 1 and should_include_frame[i] != should_include_frame[i - 1]:  # Did we flip?
            chunks.append([chunks[-1][1], i, should_include_frame[i - 1]])
    chunks.append([chunks[-1][1], audio_frame_count, should_include_frame[i - 1]])
    chunks = chunks[1:]
    output_audio_data = np.zeros((0, audioData.shape[1]))
    output_pointer = 0
    last_existing_frame = None
    for chunk in chunks:
        audio_chunk = audioData[int(chunk[0] * samples_per_frame):int(chunk[1] * samples_per_frame)]

        s_file = TEMP_FOLDER + "/tempStart.wav"
        e_file = TEMP_FOLDER + "/tempEnd.wav"
        wavfile.write(s_file, sample_rate, audio_chunk)
        with WavReader(s_file) as reader:
            with WavWriter(e_file, reader.channels, reader.samplerate) as writer:
                tsm = phasevocoder(reader.channels, speed=new_speed[int(chunk[2])])
                tsm.run(reader, writer)
        _, alteredAudioData = wavfile.read(e_file)
        leng = alteredAudioData.shape[0]
        endPointer = output_pointer + leng
        output_audio_data = np.concatenate((output_audio_data, alteredAudioData / maxAudioVolume))

        # output_audio_data[output_pointer:endPointer] = alteredAudioData/maxAudioVolume

        # smooth out transitiion's audio by quickly fading in/out

        if leng < AUDIO_FADE_ENVELOPE_SIZE:
            output_audio_data[output_pointer:endPointer] = 0  # audio is less than 0.01 sec, let's just remove it.
        else:
            premask = np.arange(AUDIO_FADE_ENVELOPE_SIZE) / AUDIO_FADE_ENVELOPE_SIZE
            mask = np.repeat(premask[:, np.newaxis], 2, axis=1)  # make the fade-envelope mask stereo
            output_audio_data[output_pointer:output_pointer + AUDIO_FADE_ENVELOPE_SIZE] *= mask
            output_audio_data[endPointer - AUDIO_FADE_ENVELOPE_SIZE:endPointer] *= 1 - mask

        startOutputFrame = int(math.ceil(output_pointer / samples_per_frame))
        endOutputFrame = int(math.ceil(endPointer / samples_per_frame))
        for outputFrame in range(startOutputFrame, endOutputFrame):
            inputFrame = int(chunk[0] + new_speed[int(chunk[2])] * (outputFrame - startOutputFrame))
            didItWork = copy_frame(inputFrame, outputFrame)
            if didItWork:
                last_existing_frame = inputFrame
            else:
                copy_frame(last_existing_frame, outputFrame)

        output_pointer = endPointer
    wavfile.write(TEMP_FOLDER + "/audioNew.wav", sample_rate, output_audio_data)
    '''
    outputFrame = math.ceil(output_pointer/samples_per_frame)
    for endGap in range(outputFrame,audio_frame_count):
        copy_frame(int(audioSampleCount/samples_per_frame)-1,endGap)
    '''
    command = "ffmpeg -framerate {0} -i {1}/newFrame%06d.jpg -i {2}/audioNew.wav -strict -2 {3} -thread_queue_size 16".format(
        str(frame_rate), TEMP_FOLDER, TEMP_FOLDER, output_file)
    subprocess.call(command, shell=True)
    deletePath(TEMP_FOLDER)


def count_mp4_files_in_folder(input_path: str):
    return len(glob.glob1(input_path, "*.mp4"))


def process_folder(output_file: str, silent_threshold: float, new_speed: list, frame_spreadage: float,
                   sample_rate: float, frame_rate: float, frame_quality: int, input_path: str):
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
