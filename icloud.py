import os
import platform

def icloud_set_bundleid(bundleid):
    global icloudbundleid
    icloudbundleid = bundleid

def set_folder(folder):
    global icloudfolder
    icloudfolder = folder


def will_work():
    if platform.mac_ver()[0].startswith('10.10') and os.path.isdir(os.path.expanduser('~/Library/Mobile Documents')):
        global icloudpath
        icloudpath = os.path.expanduser('~/Library/Mobile Documents/' + icloudbundleid + '/' + icloudfolder)
        if not os.path.isdir(icloudpath):
            os.path.mkdirs(icloudpath)
        return True
    return False

def get_file_names():
    return os.listdir(icloudpath)

def get_file_timestamp(filename):
    return int(os.path.getmtime(icloudpath + '/' + filename))

def get_file_size(filename):
    return os.stat(icloudpath + '/' + filename).st_size

def read_file(filename):
    with open(icloudpath + '/' + filename) as fileobject:
        data = fileobject.read()
    return data

def write_file(filename, data):
    with open(icloudpath + '/' + filename, 'w') as fileobject:
        fileobject.write(data)
