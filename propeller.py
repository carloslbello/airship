import os
import sys
import ctypes
import re

steamapi = ctypes.CDLL('CSteamworks.dylib')
init = steamapi.InitSafe
init.restype = ctypes.c_bool
get_file_count = steamapi.ISteamRemoteStorage_GetFileCount
get_file_name_and_size = steamapi.ISteamRemoteStorage_GetFileNameAndSize
get_file_name_and_size.restype = ctypes.c_char_p
get_file_size = steamapi.ISteamRemoteStorage_GetFileSize
get_file_timestamp = steamapi.ISteamRemoteStorage_GetFileTimestamp
file_write = steamapi.ISteamRemoteStorage_FileWrite
file_read = steamapi.ISteamRemoteStorage_FileRead

os.environ['SteamAppId'] = sys.argv[1]

if init():
    icloudPath = os.path.expanduser('~/Library/Mobile Documents/' + sys.argv[2] + '/' + sys.argv[3])

    icloudDictionary = {}
    steamDictionary = {}

    for icloudFile in os.listdir(icloudPath):
        if re.match(sys.argv[4], icloudFile):
            icloudDictionary[icloudFile] = int(os.path.getmtime(icloudPath + '/' + icloudFile))

    for steamFileIndex in range(get_file_count()):
        steamFile = get_file_name_and_size(steamFileIndex, None)
        if steamFile.startswith(sys.argv[3] + '/'):
            steamFileName = steamFile[len(sys.argv[3]) + 1:]
            if re.match(sys.argv[4], steamFileName):
                steamDictionary[steamFileName] = get_file_timestamp(steamFile)

    def modTime(file):
        modTime = get_file_timestamp(sys.argv[3] + '/' + file)
        os.utime(icloudPath + '/' + file, (modTime, modTime))

    for file in icloudDictionary:
        if not file in steamDictionary or icloudDictionary[file] > steamDictionary[file]:
            fileSize = os.path.getsize(icloudPath + '/' + file)
            fileBuffer = ctypes.create_string_buffer(fileSize)
            with open(icloudPath + '/' + file, 'r') as fileObject:
                fileBuffer.value = fileObject.read()
            file_write(sys.argv[3] + '/' + file, fileBuffer, fileSize)
            modTime(file)

    for file in steamDictionary:
        if not file in icloudDictionary or steamDictionary[file] > icloudDictionary[file]:
            fileSize = get_file_size(file)
            fileBuffer = ctypes.create_string_buffer(fileSize)
            file_read(sys.argv[3] + '/' + file, fileBuffer, fileSize)
            with open(icloudPath + '/' + file, 'w') as fileObject:
                fileObject.write(fileBuffer.value)
            modTime(file)
