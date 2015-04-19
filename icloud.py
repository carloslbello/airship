import os
import platform

def set_id(bundleid):
    global icloudbundleid
    icloudbundleid = bundleid

def set_folder(folder):
    global icloudfolder
    icloudfolder = folder

def will_work():
    if platform.system() == 'Darwin' and platform.mac_ver()[0].startswith('10.10') and os.path.isdir(os.path.expanduser('~/Library/Mobile Documents')):
        global icloudpath
        if 'icloudfolder' in globals():
            icloudpath = os.path.expanduser('~/Library/Mobile Documents/' + icloudbundleid + '/' + icloudfolder)
        else:
            icloudpath = os.path.expanduser('~/Library/Mobile Documents/' + icloudbundleid)
        if not os.path.isdir(icloudpath):
            os.path.mkdirs(icloudpath)
        return True
    return False

def get_file_names():
    return os.listdir(icloudpath)

def get_file_timestamp(filename):
    return int(os.path.getmtime(icloudpath + '/' + filename))

def read_file(filename):
    with open(icloudpath + '/' + filename) as fileobject:
        data = fileobject.read()
    return data

def write_file(filename, data):
    with open(icloudpath + '/' + filename, 'w') as fileobject:
        fileobject.write(data)
