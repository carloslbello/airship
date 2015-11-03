import platform
import os

try:
    from scandir import walk
except ImportError:
    from os import walk
    
def init():
    global icloudfolder
    icloudfolder = ''

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

    for folder, _, files in walk(icloudpath):
        for filename in files:
            filenames.append((folder + '/' + filename)[len(icloudpath) + 1:])

    return filenames

def get_file_timestamp(filename):
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
