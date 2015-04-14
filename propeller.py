import argparse
import sys
import os
import importlib
import re
import time
import hashlib

parser = argparse.ArgumentParser(description = 'Helper process for airship.py. Not meant for manual use.')
parser.add_argument('--folder', required = True)
parser.add_argument('--regex', required = True)
parser.add_argument('--steamappid')
parser.add_argument('--icloudbundleid')

arguments = parser.parse_args(sys.argv[1:])

modules = []

def add_module(modulename):
    module = importlib.import_module(modulename)
    module.set_folder(arguments.folder)

    if modulename == 'steamcloud':
        module.steamcloud_set_appid(arguments.steamappid)
    if modulename == 'icloud':
        module.icloud_set_bundleid(arguments.icloudbundleid)

    if module.will_work():
        modules.append(module)

if 'steamappid' in arguments:
    add_module('steamcloud')

if 'icloudbundleid' in arguments:
    add_module('icloud')

filetimestamps = {}

if len(modules) > 1:
    for moduleindex in range(len(modules)):
        filenames = modules[moduleindex].get_file_names()
        for filename in filenames:
            if re.match(arguments.regex, filename):
                if not filename in filetimestamps:
                    filetimestamps[filename] = [0] * len(modules)
                filetimestamps[filename][moduleindex] = modules[moduleindex].get_file_timestamp(filename)

    for filename in filetimestamps:
        newerfilesmayexist = True
        highestlowtimestamp = -1
        while newerfilesmayexist:
            newerfilesmayexist = False
            lowesttimestamp = int(time.time())
            lowesttimestampindex = -1
            for moduleindex in range(len(modules)):
                if highestlowtimestamp < filetimestamps[filename][moduleindex] < lowesttimestamp:
                    lowesttimestamp = filetimestamps[filename][moduleindex]
                    lowesttimestampindex = moduleindex
            if lowesttimestampindex != -1:
                newerfilesmayexist = True
                highestlowtimestamp = lowesttimestamp
                originaldata = modules[lowesttimestampindex].read_file(filename)
                for moduleindex in range(len(modules)):
                    if moduleindex != lowesttimestampindex and modules[moduleindex].read_file(filename) == originaldata:
                        filetimestamps[filename][moduleindex] = lowesttimestamp
                        
        highesttimestamp = -1
        highesttimestampindex = -1
        for moduleindex in range(len(modules)):
            if filetimestamps[filename][moduleindex] > highesttimestamp:
                highesttimestamp = filetimestamps[filename][moduleindex]
                highesttimestampindex = moduleindex
        highesttimestampdata = modules[highesttimestampindex].read_file(filename)
        for moduleindex in range(len(modules)):
            if moduleindex != highesttimestampindex and filetimestamps[filename][moduleindex] < highesttimestamp:
                modules[moduleindex].file_write(filename, highesttimestampdata)
