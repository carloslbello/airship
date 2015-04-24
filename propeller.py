import argparse
import sys
import os
import importlib
import re
import time
import hashlib

parser = argparse.ArgumentParser(description='Helper process for airship.py. Not meant for manual use.')
parser.add_argument('--regex', required=True)
parser.add_argument('--folder')

possiblemodules = ['icloud', 'steamcloud']

for modulename in possiblemodules:
    parser.add_argument('--' + modulename + 'id')
    parser.add_argument('--' + modulename + 'folder')

arguments = vars(parser.parse_args(sys.argv[1:]))

modules = []

def add_module(modulename):
    try:
        module = importlib.import_module(modulename)

        if arguments[modulename + 'folder'] is not None or arguments['folder'] is not None:
            module.set_folder(arguments[modulename + 'folder'] if arguments[modulename + 'folder'] is not None else arguments['folder'])

        module.set_id(arguments[modulename + 'id'])

        if module.will_work():
            modules.append(module)
    except:
        pass

for modulename in possiblemodules:
    if arguments[modulename + 'id'] is not None:
        add_module(modulename)

filetimestamps = {}

if len(modules) > 1:
    for moduleindex in range(len(modules)):
        filenames = modules[moduleindex].get_file_names()
        for filename in filenames:
            if re.match(arguments['regex'], filename):
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
                if originaldata is not None:
                    originalhash = hashlib.sha1(originaldata).hexdigest()
                    for moduleindex in range(len(modules)):
                        if moduleindex != lowesttimestampindex and hashlib.sha1(modules[moduleindex].read_file(filename)).hexdigest() == originalhash:
                            filetimestamps[filename][moduleindex] = lowesttimestamp

        highesttimestamp = -1
        highesttimestampindex = -1
        for moduleindex in range(len(modules)):
            if filetimestamps[filename][moduleindex] > highesttimestamp:
                highesttimestamp = filetimestamps[filename][moduleindex]
                highesttimestampindex = moduleindex
        highesttimestampdata = modules[highesttimestampindex].read_file(filename)
        if highesttimestampdata is not None:
            for moduleindex in range(len(modules)):
                if moduleindex != highesttimestampindex and filetimestamps[filename][moduleindex] < highesttimestamp:
                    modules[moduleindex].write_file(filename, highesttimestampdata)
