import platform
import subprocess
import re
import os

def init():
    global icloudfolder
    icloudfolder = None
    global icloudfilesnotinsync
    icloudfilesnotinsync = []

    def compareversion(version1, version2): # http://stackoverflow.com/a/1714190/4270716
        def normalize(v):
            return [int(x) for x in re.sub(r'(\.0+)*$','', v).split(".")]
        version1n = normalize(version1)
        version2n = normalize(version2)
        return (version1n > version2n) - (version1n < version2n)

    if platform.system() == 'Darwin':
        product = subprocess.check_output(['sw_vers', '-productName']).decode('utf-8')
        version = subprocess.check_output(['sw_vers', '-productVersion']).decode('utf-8')
        return (product == 'Mac OS X\n' and compareversion(version, '10.10') >= 0) or (product == 'iPhone OS\n' and compareversion(version, '8') >= 0) and os.path.isdir(os.path.expanduser('~/Library/Mobile Documents'))
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
    def recursive_dir_contents(dir):
        dircontents = os.listdir(icloudpath if dir is None else icloudpath + '/' + dir)
        for item in dircontents:
            if os.path.isdir(icloudpath + '/' + item if dir is None else icloudpath + '/' + dir + '/' + item):
                recursive_dir_contents(item if dir is None else dir + '/' + item)
            else:
                filenames.append(item if dir is None else dir + '/' + item)

    recursive_dir_contents(None)

    for filename in filenames:
        match = re.match('^([^/]+/)?\.([^/]+)\.icloud$', filename)
        if match:
            filenames.remove(filename)
            actualfilename = (match.group(1) if match.group(1) else '') + match.group(2)
            filenames.append(actualfilename)
            icloudfilesnotinsync.append(actualfilename)

    return filenames

def get_file_timestamp(filename):
    if filename in icloudfilesnotinsync:
        return 0
    else:
        return int(os.path.getmtime(icloudpath + '/' + filename))

def read_file(filename):
    with open(icloudpath + '/' + filename) as fileobject:
        data = fileobject.read()
    return data

def write_file(filename, data):
    path = icloudpath + '/' + filename
    directory = path[:path.rfind('/')]

    if not os.path.isdir(directory):
        os.makedirs(directory)

    with open(path, 'w') as fileobject:
        fileobject.write(data)

def shutdown():
    global icloudfolder
    icloudfolder = None
    global icloudfilesnotinsync
    icloudfilesnotinsync = []
