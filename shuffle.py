#!/usr/bin/env python

import argparse
import os
import random
import subprocess
import shutil

parser = argparse.ArgumentParser()
parser.add_argument("source_directory")
parser.add_argument("target_directory")
parser.add_argument("--duration", type=float, default=75,
                    help="Duration in minutes")
args = parser.parse_args()

if not os.path.exists(args.target_directory):
    raise Exception("Target directory '%s' does not exist." % args.target_directory)

if not os.path.isdir(args.target_directory):
    raise Exception("'%s' is not a directory." % args.target_directory)

def get_audio_files(root_path):
    for dirpath, dirnames, filenames in os.walk(root_path):
        for filename in filenames:
            filepath = "%s/%s" % (dirpath, filename)
            if is_audio_file(filepath):
                yield dirpath, filename

def is_audio_file(filename):
    return filename.endswith(".mp3")

def get_duration_seconds(filename):
    process = subprocess.Popen(
        ["soxi", "-D", filename], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout_data, stderr_data = process.communicate()
    stdout_data = stdout_data.rstrip("\n")
    return float(stdout_data)

audio_files_in_source = list(get_audio_files(args.source_directory))
random.shuffle(audio_files_in_source)

selected_duration_seconds = 0
target_audio_files = []
target_duration_seconds = args.duration * 60
while selected_duration_seconds < target_duration_seconds:
    dirpath, filename = audio_files_in_source.pop(0)
    filepath = "%s/%s" % (dirpath, filename)
    selected_duration_seconds += get_duration_seconds(filepath)
    target_audio_files.append((dirpath, filename))

index = 1
for dirpath, filename in target_audio_files:
    shutil.copyfile(
        "%s/%s" % (dirpath, filename),
        "%s/%03d_%s" % (args.target_directory, index, filename))
    index += 1
