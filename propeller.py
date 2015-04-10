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
if init():
    icloudPath = os.path.expanduser("~/Library/Mobile Documents/" + sys.argv[2])
    icloudDictionary = {}
    steamDictionary = {}
    for icloudFile in os.listdir(icloudPath):
        if re.match(sys.argv[4], icloudFile):
            icloudDictionary[icloudFile] = int(os.path.getmtime(icloudPath + "/" + icloudFile))
    steamFileNum = getFileCount()
    for steamFileIndex in range(0, steamFileNum):
        steamFile = getFileNameAndSize(steamFileIndex, None)
        steamFileName = steamFile[len(sys.argv[3]) + 1:]
        if re.match(sys.argv[4], steamFileName) and steamFile.startswith(sys.argv[3] + "/"):
            steamDictionary[steamFileName] = getFileTimestamp(steamFile)
    def modTime(file):
        modTime = getFileTimestamp(sys.argv[3] + "/" + file)
        os.utime(icloudPath + "/" + file, (modTime, modTime))
    for file in icloudDictionary:
        if not file in steamDictionary or icloudDictionary[file] > steamDictionary[file]:
            fileSize = os.path.getsize(icloudPath + "/" + file)
            fileBuffer = ctypes.create_string_buffer(fileSize)
            fileObject = open(icloudPath + "/" + file, "r")
            fileBuffer.value = fileObject.read()
            fileObject.close()
            fileWrite(sys.argv[3] + "/" + file, fileBuffer, fileSize)
            modTime(file)
    for file in steamDictionary:
        if not file in icloudDictionary or steamDictionary[file] > icloudDictionary[file]:
            fileSize = getFileSize(file)
            fileBuffer = ctypes.create_string_buffer(fileSize)
            fileRead(sys.argv[3] + "/" + file, fileBuffer, fileSize)
            fileObject = open(icloudPath + "/" + file, "w")
            fileObject.write(fileBuffer.value)
            fileObject.close()
            modTime(file)
