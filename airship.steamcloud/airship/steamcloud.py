import os
import platform
import ctypes

def init():
    try:
        system = platform.system()
        bits = platform.architecture()[0][:2]

        global steamapi
        if system == 'Windows':
            steamapi = ctypes.CDLL('bin_win' + bits + '/CSteamworks.dll')
        elif system == 'Darwin':
            steamapi = ctypes.CDLL('bin_osx/CSteamworks.dylib')
        else:
            steamapi = ctypes.CDLL('bin_lnx' + bits + '/libCSteamworks.so')

        global steamapi_init
        steamapi_init = steamapi.InitSafe
        steamapi_init.restype = ctypes.c_bool
        global steamapi_get_file_count
        steamapi_get_file_count = steamapi.ISteamRemoteStorage_GetFileCount
        steamapi_get_file_count.restype = ctypes.c_int
        global steamapi_get_file_name_size
        steamapi_get_file_name_size = steamapi.ISteamRemoteStorage_GetFileNameAndSize
        steamapi_get_file_name_size.restype = ctypes.c_char_p
        global steamapi_get_file_size
        steamapi_get_file_size = steamapi.ISteamRemoteStorage_GetFileSize
        global steamapi_get_file_timestamp
        steamapi_get_file_timestamp = steamapi.ISteamRemoteStorage_GetFileTimestamp
        global steamapi_file_write
        steamapi_file_write = steamapi.ISteamRemoteStorage_FileWrite
        global steamapi_file_read
        steamapi_file_read = steamapi.ISteamRemoteStorage_FileRead
        global steamapi_shutdown
        steamapi_shutdown = steamapi.Shutdown

        global steamfolder
        steamfolder = None

        return True

    except:
        return False


def set_id(appid):
    os.environ['SteamAppId'] = appid

def set_folder(folder):
    global steamfolder
    steamfolder = folder

def will_work():
    return steamapi_init()

def get_file_names():
    filenames = []

    for fileindex in range(steamapi_get_file_count()):
        filename = steamapi_get_file_name_size(fileindex, None)
        if steamfolder is not None:
            if filename.startswith(steamfolder + '/'):
                filenames.append(filename[len(steamfolder) + 1:])
        else:
            filenames.append(filename)
    return filenames

def get_file_timestamp(filename):
    return steamapi_get_file_timestamp(('' if steamfolder is None else steamfolder + '/') + filename)

def read_file(filename):
    size = steamapi_get_file_size(('' if steamfolder is None else steamfolder + '/') + filename)
    buffer = ctypes.create_string_buffer(size)
    steamapi_file_read(('' if steamfolder is None else steamfolder + '/') + filename, buffer, size)
    return buffer.value

def write_file(filename, data):
    size = len(data)
    buffer = ctypes.create_string_buffer(size)
    buffer.value = data
    steamapi_file_write(('' if steamfolder is None else steamfolder + '/') + filename, buffer, size)

def shutdown():
    global steamfolder
    steamfolder = None
    steamapi_shutdown()
