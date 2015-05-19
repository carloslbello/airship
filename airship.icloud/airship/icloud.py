import platform
import subprocess
import re
import os

def init():
    global icloudfolder
    icloudfolder = ''
    global icloudfilesnotinsync
    icloudfilesnotinsync = []
    global icloudplistregex
    icloudplistregex = re.compile(r'^((?:[^/]+/)*)\.([^/]+)\.icloud$')

    if platform.system() == 'Darwin':
        return os.path.isdir(os.path.expanduser('~/Library/Mobile Documents'))

    else:
        return False

def set_id(bundleid):
    global icloudbundleid
    icloudbundleid = bundleid

def set_folder(folder):
    global icloudfolder
    icloudfolder = folder

def will_work():
    global icloudpath
    icloudpath = os.path.expanduser('~/Library/Mobile Documents/' + icloudbundleid + ('/' + icloudfolder if icloudfolder else ''))

    return os.path.isdir(icloudpath)

def get_file_names():
    filenames = []

    def recursive_dir_contents(directory):
        dircontents = os.listdir(icloudpath + ('/' + directory if directory else ''))
        for item in dircontents:
            if os.path.isdir(icloudpath + ('/' + directory if directory else '') + '/' + item):
                recursive_dir_contents((directory + '/' if directory else '') + item)
            else:
                filenames.append((directory + '/' if directory else '') + item)

    recursive_dir_contents('')

    for filename in filenames:
        match = icloudplistregex.match(filename)
        if match:
            filenames.remove(filename)
            icloudfilesnotinsync.append((match.group(1) if match.group(1) else '') + match.group(2))

    return filenames + icloudfilesnotinsync

def get_file_timestamp(filename):
    if filename in icloudfilesnotinsync:
        return 0
    else:
        return int(os.path.getmtime(icloudpath + '/' + filename))

def read_file(filename):
    with open(icloudpath + '/' + filename, 'rb') as fileobject:
        data = fileobject.read()
    return data

def write_file(filename, data):
    path = icloudpath + '/' + filename
    directory = os.path.dirname(path)

    if not os.path.isdir(directory):
        os.makedirs(directory)

    with open(path, 'wb') as fileobject:
        fileobject.write(data)

def shutdown():
    global icloudfolder
    icloudfolder = ''
    global icloudfilesnotinsync
    icloudfilesnotinsync = []
