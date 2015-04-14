import os
import platform
import ctypes

def steamcloud_set_appid(appid):
    os.environ['SteamAppId'] = appid

def set_folder(folder):
    global steamfolder
    steamfolder = folder

def will_work():
    try:
        system = platform.system()

        if system == 'Windows':
            steamapi = ctypes.CDLL('bin_win/CSteamworks.dll')
        elif system == 'Darwin':
            steamapi = ctypes.CDLL('bin_osx/CSteamworks.dylib')
        else:
            steamapi = ctypes.CDLL('bin_lnx/CSteamworks.so')

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

        return steamapi_init()

    except:
        return False

def get_file_names():
    filenames = []
    for fileindex in range(steamapi_get_file_count()):
        filename = steamapi_get_file_name_size(fileindex, None)
        if filename.startswith(steamfolder + '/'):
            filenames.append(filename[len(steamfolder) + 1:])
    return filenames

def get_file_timestamp(filename):
    return steamapi_get_file_timestamp(steamfolder + '/' + filename)

def get_file_size(filename):
    return steamapi_get_file_size(steamfolder + '/' + filename)

def read_file(filename):
    size = get_file_size(filename)
    buffer = ctypes.create_string_buffer(size)
    steamapi_file_read(steamfolder + '/' + filename, buffer, size)
    return buffer.value

def write_file(filename, data):
    size = len(data)
    buffer = ctypes.create_string_buffer(size)
    buffer.value = data
    steamapi_file_write(steamfolder + '/' + filename, buffer, size)
