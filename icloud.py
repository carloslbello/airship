import os
import platform

def set_id(bundleid):
    global icloudbundleid
    icloudbundleid = bundleid

def set_folder(folder):
    global icloudfolder
    icloudfolder = folder

def will_work():
    if platform.mac_ver()[0].startswith('10.10') and os.path.isdir(os.path.expanduser('~/Library/Mobile Documents')):
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
    filenames = []
    def recursive_dir_contents(dir):
        dircontents = os.listdir(icloudpath if dir is None else icloudpath + '/' + dir )
        for item in dircontents:
            if os.path.isdir(icloudpath + '/' + item if dir is None else icloudpath + '/' + dir + '/' + item):
                recursive_dir_contents(item if dir is None else dir + '/' + item)
            else:
                filenames.append(item if dir is None else dir + '/' + item)

    recursive_dir_contents(None)
    return filenames

def get_file_timestamp(filename):
    return int(os.path.getmtime(icloudpath + '/' + filename))

def read_file(filename):
    with open(icloudpath + '/' + filename) as fileobject:
        data = fileobject.read()
    return data

def write_file(filename, data):
    with open(icloudpath + '/' + filename, 'w') as fileobject:
        fileobject.write(data)
