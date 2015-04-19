import os
import platform
import ctypes

def set_id(appid):
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
        if 'steamfolder' in globals():
            if filename.startswith(steamfolder + '/'):
                filenames.append(filename[len(steamfolder) + 1:])
        else:
            filenames.append(filename)
    return filenames

def get_file_timestamp(filename):
    if 'steamfolder' in globals():
        return steamapi_get_file_timestamp(steamfolder + '/' + filename)
    else:
        return steamapi_get_file_timestamp(filename)

def read_file(filename):
    if 'steamfolder' in globals():
        size = steamapi_get_file_size(steamfolder + '/' + filename)
    else:
        size = steamapi_get_file_size(filename)
    buffer = ctypes.create_string_buffer(size)
    if 'steamfolder' in globals():
        steamapi_file_read(steamfolder + '/' + filename, buffer, size)
    else:
        steamapi_file_read(filename, buffer, size)
    return buffer.value

def write_file(filename, data):
    size = len(data)
    buffer = ctypes.create_string_buffer(size)
    buffer.value = data
    if 'steamfolder' in globals():
        steamapi_file_write(steamfolder + '/' + filename, buffer, size)
    else:
        steamapi_file_write(filename, buffer, size)
