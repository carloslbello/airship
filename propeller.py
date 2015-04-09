#!/usr/bin/python
import os, sys, ctypes, re
os.environ["SteamAppId"] = sys.argv[1]
steamapi = ctypes.CDLL("CSteamworks.dylib")
init = steamapi.InitSafe
init.restype = ctypes.c_bool
getFileCount = steamapi.ISteamRemoteStorage_GetFileCount
getFileNameAndSize = steamapi.ISteamRemoteStorage_GetFileNameAndSize
getFileNameAndSize.restype = ctypes.c_char_p
getFileSize = steamapi.ISteamRemoteStorage_GetFileSize
getFileTimestamp = steamapi.ISteamRemoteStorage_GetFileTimestamp
fileWrite = steamapi.ISteamRemoteStorage_FileWrite
fileRead = steamapi.ISteamRemoteStorage_FileRead
if init().value:
    icloudPath = os.path.expanduser("~/Library/Mobile Documents/" + sys.argv[2])
    icloudDictionary = {}
    steamDictionary = {}
    for icloudFile in os.listdir(icloudPath):
        if re.match(sys.argv[3], icloudFile):
            icloudDictionary[icloudFile] = int(os.path.getmtime(icloudFullPath + "/" + icloudFile))
    steamFileNum = steamapi.ISteamRemoteStorage_GetFileCount().value
    for steamFileIndex in range(0, steamFileNum):
        steamFile = getFileNameAndSize(steamFileIndex, None).value
        if re.match(sys.argv[3], steamFile):
            steamDictionary[steamFile] = getFileTimestamp(steamFile)
    def modTime(file):
        modTime = getFileTimestamp(file).value
        os.utime(icloudPath + "/" + file, (modTime, modTime))
    for file in icloudDictionary:
        if not steamDictionary[file] or icloudDictionary[file] > steamDictionary[file]:
            fileSize = os.path.getsize(icloudPath + "/" + file)
            fileBuffer = ctypes.create_string_buffer(fileSize)
            fileObject = open(icloudPath + "/" + file, "r")
            fileBuffer.value = fileObject.read()
            fileObject.close()
            fileWrite(file, fileBuffer, fileSize)
            modTime(file)
    for file in steamDictionary:
        if not icloudDictionary[file] or steamDictionary[file] > icloudDictionary[file]:
            fileSize = getFileSize(file).value
            fileBuffer = ctypes.create_string_buffer(fileSize)
            fileRead(file, fileBuffer, fileSize)
            fileObject = open(icloudPath + "/" + file, "w")
            fileObject.write(fileBuffer.value)
            fileObject.close()
            modTime(file)
