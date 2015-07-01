import os
import platform
import ctypes

name = 'steamcloud'

def init():
    try:
        path = os.path.dirname(os.path.abspath(__file__))
        system = platform.system()
        bits = platform.architecture()[0][:2]

        global steamapi
        if system == 'Windows':
            steamapi = ctypes.CDLL(path + '/bin_win' + bits + '/CSteamworks.dll')
        elif system == 'Darwin':
            steamapi = ctypes.CDLL(path + '/bin_osx/CSteamworks.dylib')
        else:
            steamapi = ctypes.CDLL(path + '/bin_lnx' + bits + '/libCSteamworks.so')

        global steamapi_init
        steamapi_init = steamapi.InitSafe
        steamapi_init.restype = ctypes.c_bool
        global steamapi_get_file_count
        steamapi_get_file_count = steamapi.ISteamRemoteStorage_GetFileCount
        steamapi_get_file_count.restype = ctypes.c_int
        global steamapi_get_file_name_size
        steamapi_get_file_name_size = steamapi.ISteamRemoteStorage_GetFileNameAndSize
        steamapi_get_file_name_size.argtypes = [ctypes.c_int, ctypes.c_int]
        steamapi_get_file_name_size.restype = ctypes.c_char_p
        global steamapi_get_file_size
        steamapi_get_file_size = steamapi.ISteamRemoteStorage_GetFileSize
        steamapi_get_file_size.argtypes = [ctypes.c_char_p]
        steamapi_get_file_size.restype = ctypes.c_int
        global steamapi_get_file_timestamp
        steamapi_get_file_timestamp = steamapi.ISteamRemoteStorage_GetFileTimestamp
        steamapi_get_file_timestamp.argtypes = [ctypes.c_char_p]
        steamapi_get_file_timestamp.restype = ctypes.c_int
        global steamapi_file_write
        steamapi_file_write = steamapi.ISteamRemoteStorage_FileWrite
        steamapi_file_write.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int]
        global steamapi_file_read
        steamapi_file_read = steamapi.ISteamRemoteStorage_FileRead
        steamapi_file_read.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int]
        global steamapi_shutdown
        steamapi_shutdown = steamapi.Shutdown
        global steamapi_cloud_enabled_account
        steamapi_cloud_enabled_account = steamapi.ISteamRemoteStorage_IsCloudEnabledForAccount
        steamapi_cloud_enabled_account.restype = ctypes.c_bool
        global steamapi_cloud_enabled_app
        steamapi_cloud_enabled_app = steamapi.ISteamRemoteStorage_IsCloudEnabledForApp
        steamapi_cloud_enabled_app.restype = ctypes.c_bool

        global steamfolder
        steamfolder = ''

        is_steam_running = steamapi.IsSteamRunning
        is_steam_running.restype = ctypes.c_bool

        return is_steam_running()

    except OSError:
        return False


def set_id(appid):
    os.environ['SteamAppId'] = appid

def set_folder(folder):
    global steamfolder
    steamfolder = folder

def will_work():
    return steamapi_init() and steamapi_cloud_enabled_account() and steamapi_cloud_enabled_app()

def get_file_names():
    filenames = []

    for fileindex in range(steamapi_get_file_count()):
        filename = steamapi_get_file_name_size(fileindex, 0).decode('utf-8')
        if steamfolder:
            if filename.startswith(steamfolder + '/'):
                filenames.append(filename[len(steamfolder) + 1:])
        else:
            filenames.append(filename)
    return filenames

def get_file_timestamp(filename):
    return steamapi_get_file_timestamp(((steamfolder + '/' if steamfolder else '') + filename).encode('utf-8'))

def read_file(filename):
    size = steamapi_get_file_size(((steamfolder + '/' if steamfolder else '') + filename).encode('utf-8'))
    stringbuffer = ctypes.create_string_buffer(size)
    steamapi_file_read(((steamfolder + '/' if steamfolder else '') + filename).encode('utf-8'), stringbuffer, size)
    return None if not stringbuffer.value else bytearray(stringbuffer)

def write_file(filename, data):
    size = len(data)
    stringbuffer = ctypes.create_string_buffer(bytes(data))
    steamapi_file_write(((steamfolder + '/' if steamfolder else '') + filename).encode('utf-8'), stringbuffer, size)

def shutdown():
    global steamfolder
    steamfolder = ''
    steamapi_shutdown()
