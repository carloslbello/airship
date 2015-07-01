import platform
import os

try:
    from os import scandir
except ImportError:
    try:
        from scandir import scandir
    except ImportError:
        pass

name = 'icloud'

def init():
    global icloudfolder
    icloudfolder = ''
    global icloudfilesnotinsync
    icloudfilesnotinsync = []

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

    if 'scandir' in globals():
        def recursive_dir_contents(directory):
            for entry in scandir(icloudpath + ('/' + directory if directory else '')):
                if entry.is_dir():
                    recursive_dir_contents((directory + '/' if directory else '') + entry.name)
                else:
                    if entry.name.startswith('.') and entry.name.endswith('.icloud'):
                        icloudfilesnotinsync.append((directory + '/' if directory else '') + entry.name[1:-7])
                    else:
                        filenames.append((directory + '/' if directory else '') + entry.name)
    else:
        def recursive_dir_contents(directory):
            for entry in os.listdir(icloudpath + ('/' + directory if directory else '')):
                if os.path.isdir(icloudpath + ('/' + directory if directory else '') + '/' + entry):
                    recursive_dir_contents((directory + '/' if directory else '') + entry)
                else:
                    if entry.startswith('.') and entry.endswith('.icloud'):
                        icloudfilesnotinsync.append((directory + '/' if directory else '') + entry[1:-7])
                    else:
                        filenames.append((directory + '/' if directory else '') + entry)

    recursive_dir_contents('')

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
