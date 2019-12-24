import math
import os
import re
import subprocess
from shutil import copyfile, rmtree

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


def process(OUTPUT_FILE: str, SILENT_THRESHOLD: float, NEW_SPEED: list, FRAME_SPREADAGE: float,
            SAMPLE_RATE: float, frameRate: float, FRAME_QUALITY: int, INPUT_FILE: str):
    global TEMP_FOLDER
    assert INPUT_FILE is not None, "why u put no input file, that dum"
    if len(OUTPUT_FILE) < 1:
        OUTPUT_FILE = input_to_output_filename(INPUT_FILE)

    # smooth out transitiion's audio by quickly fading in/out (arbitrary magic number whatever)
    AUDIO_FADE_ENVELOPE_SIZE = 400
    create_path(TEMP_FOLDER)
    command = "ffmpeg -i " + INPUT_FILE + " -qscale:v " + str(
        FRAME_QUALITY) + " " + TEMP_FOLDER + "/frame%06d.jpg -hide_banner"
    subprocess.call(command, shell=True)
    command = "ffmpeg -i " + INPUT_FILE + " -ab 160k -ac 2 -ar " + str(
        SAMPLE_RATE) + " -vn " + TEMP_FOLDER + "/audio.wav"
    subprocess.call(command, shell=True)
    command = "ffmpeg -i " + TEMP_FOLDER + "/input.mp4 2>&1"
    f = open(TEMP_FOLDER + "/params.txt", "w")
    subprocess.call(command, shell=True, stdout=f)
    sampleRate, audioData = wavfile.read(TEMP_FOLDER + "/audio.wav")
    audioSampleCount = audioData.shape[0]
    maxAudioVolume = get_max_volume(audioData)
    f = open(TEMP_FOLDER + "/params.txt", 'r+')
    pre_params = f.read()
    f.close()
    params = pre_params.split('\n')
    for line in params:
        m = re.search('Stream #.*Video.* ([0-9]*) fps', line)
        if m is not None:
            frameRate = float(m.group(1))
    samplesPerFrame = sampleRate / frameRate
    audioFrameCount: int = int(math.ceil(audioSampleCount / samplesPerFrame))
    hasLoudAudio = np.zeros(audioFrameCount)
    i: int
    for i in range(audioFrameCount):
        start = int(i * samplesPerFrame)
        end = min(int((i + 1) * samplesPerFrame), audioSampleCount)
        audiochunks = audioData[start:end]
        maxchunksVolume = float(get_max_volume(audiochunks)) / maxAudioVolume
        if maxchunksVolume >= SILENT_THRESHOLD:
            hasLoudAudio[i] = 1
    chunks = [[0, 0, 0]]
    shouldIncludeFrame = np.zeros(audioFrameCount)
    for i in range(audioFrameCount):
        start = int(max(0, i - FRAME_SPREADAGE))
        end = int(min(audioFrameCount, i + 1 + FRAME_SPREADAGE))
        shouldIncludeFrame[i] = np.max(hasLoudAudio[start:end])
        if i >= 1 and shouldIncludeFrame[i] != shouldIncludeFrame[i - 1]:  # Did we flip?
            chunks.append([chunks[-1][1], i, shouldIncludeFrame[i - 1]])
    chunks.append([chunks[-1][1], audioFrameCount, shouldIncludeFrame[i - 1]])
    chunks = chunks[1:]
    outputAudioData = np.zeros((0, audioData.shape[1]))
    outputPointer = 0
    lastExistingFrame = None
    for chunk in chunks:
        audioChunk = audioData[int(chunk[0] * samplesPerFrame):int(chunk[1] * samplesPerFrame)]

        sFile = TEMP_FOLDER + "/tempStart.wav"
        eFile = TEMP_FOLDER + "/tempEnd.wav"
        wavfile.write(sFile, SAMPLE_RATE, audioChunk)
        with WavReader(sFile) as reader:
            with WavWriter(eFile, reader.channels, reader.samplerate) as writer:
                tsm = phasevocoder(reader.channels, speed=NEW_SPEED[int(chunk[2])])
                tsm.run(reader, writer)
        _, alteredAudioData = wavfile.read(eFile)
        leng = alteredAudioData.shape[0]
        endPointer = outputPointer + leng
        outputAudioData = np.concatenate((outputAudioData, alteredAudioData / maxAudioVolume))

        # outputAudioData[outputPointer:endPointer] = alteredAudioData/maxAudioVolume

        # smooth out transitiion's audio by quickly fading in/out

        if leng < AUDIO_FADE_ENVELOPE_SIZE:
            outputAudioData[outputPointer:endPointer] = 0  # audio is less than 0.01 sec, let's just remove it.
        else:
            premask = np.arange(AUDIO_FADE_ENVELOPE_SIZE) / AUDIO_FADE_ENVELOPE_SIZE
            mask = np.repeat(premask[:, np.newaxis], 2, axis=1)  # make the fade-envelope mask stereo
            outputAudioData[outputPointer:outputPointer + AUDIO_FADE_ENVELOPE_SIZE] *= mask
            outputAudioData[endPointer - AUDIO_FADE_ENVELOPE_SIZE:endPointer] *= 1 - mask

        startOutputFrame = int(math.ceil(outputPointer / samplesPerFrame))
        endOutputFrame = int(math.ceil(endPointer / samplesPerFrame))
        for outputFrame in range(startOutputFrame, endOutputFrame):
            inputFrame = int(chunk[0] + NEW_SPEED[int(chunk[2])] * (outputFrame - startOutputFrame))
            didItWork = copy_frame(inputFrame, outputFrame)
            if didItWork:
                lastExistingFrame = inputFrame
            else:
                copy_frame(lastExistingFrame, outputFrame)

        outputPointer = endPointer
    wavfile.write(TEMP_FOLDER + "/audioNew.wav", SAMPLE_RATE, outputAudioData)
    '''
    outputFrame = math.ceil(outputPointer/samplesPerFrame)
    for endGap in range(outputFrame,audioFrameCount):
        copy_frame(int(audioSampleCount/samplesPerFrame)-1,endGap)
    '''
    command = "ffmpeg -framerate " + str(
        frameRate) + " -i " + TEMP_FOLDER + "/newFrame%06d.jpg -i " + TEMP_FOLDER + "/audioNew.wav -strict -2 " + OUTPUT_FILE
    subprocess.call(command, shell=True)
    deletePath(TEMP_FOLDER)
