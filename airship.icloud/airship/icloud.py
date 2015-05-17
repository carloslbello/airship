import platform
import subprocess
import re
import os

def init():
    global icloudfolder
    icloudfolder = None
    global icloudfilesnotinsync
    icloudfilesnotinsync = []
    global icloudplistregex
    icloudplistregex = re.compile(r'^((?:[^/]+/)*)\.([^/]+)\.icloud$')

    def normalize(v): # http://stackoverflow.com/a/1714190/4270716
        return [int(x) for x in re.sub(r'(\.0+)*$', '', v).split('.')]

    if platform.system() == 'Darwin':
        product = subprocess.check_output(['sw_vers', '-productName']).decode('utf-8')[:-1]
        version = normalize(subprocess.check_output(['sw_vers', '-productVersion']).decode('utf-8')[:-1])
        return (product == 'Mac OS X' and version >= [10, 10]) or (product == 'iPhone OS' and version >= [8]) and os.path.isdir(os.path.expanduser('~/Library/Mobile Documents'))
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
    icloudpath = os.path.expanduser('~/Library/Mobile Documents/' + icloudbundleid + ('' if icloudfolder is None else '/' + icloudfolder))

    return os.path.isdir(icloudpath)

def get_file_names():
    filenames = []

    def recursive_dir_contents(directory):
        dircontents = os.listdir(icloudpath if directory is None else icloudpath + '/' + directory)
        for item in dircontents:
            if os.path.isdir(icloudpath + '/' + item if directory is None else icloudpath + '/' + directory + '/' + item):
                recursive_dir_contents(item if directory is None else directory + '/' + item)
            else:
                filenames.append(item if directory is None else directory + '/' + item)

    recursive_dir_contents(None)

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
    directory = path[:path.rfind('/')]

    if not os.path.isdir(directory):
        os.makedirs(directory)

    with open(path, 'wb') as fileobject:
        fileobject.write(data)

def shutdown():
    global icloudfolder
    icloudfolder = None
    global icloudfilesnotinsync
    icloudfilesnotinsync = []
