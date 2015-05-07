import platform
import distutils.version
import os

def init():
    global icloudfolder
    icloudfolder = None

    if platform.system() == 'Darwin':
        version, _, machine = platform.mac_ver()
        version = distutils.version.StrictVersion(version)
        return version > distutils.version.StrictVersion('10.10') and os.path.isdir(os.path.expanduser('~/Library/Mobile Documents'))

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
    def recursive_dir_contents(dir):
        dircontents = os.listdir(icloudpath if dir is None else icloudpath + '/' + dir)
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
    path = icloudpath + '/' + filename
    dir = path[:path.rfind('/')]

    if not os.path.isdir(dir):
        os.makedirs(dir)

    with open(path, 'w') as fileobject:
        fileobject.write(data)

def shutdown():
    global icloudfolder
    icloudfolder = None
