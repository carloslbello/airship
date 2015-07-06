from __future__ import division
import importlib
import re
import zlib
import io

try:
    import PIL.Image
    imagemanip = True
except ImportError:
    imagemanip = False

# Data manipulation functions

# Identity

def identity_read(filename, timestamp, data, origin):
    return ([(filename, timestamp, data)], {})

def identity_compare(filename, data1, data2):
    return data1 == data2

def identity_write(filename, data, destination):
    return (filename, data)

def noop_after(filedata, modules, metadata):
    pass

# The Banner Saga

def bannersaga_transform_argb_rgb(orig):
    result = bytearray()
    orig = orig[13:]
    for i in range(len(orig) // 4):
        byteindex = i * 4
        result += orig[byteindex + 1:byteindex + 4]
    return bytes(result)

def bannersaga_transform_rgb_argb(orig):
    result = bytearray(b'\x00\x00\x01\xe0\x00\x00\x01h\x00\x00\x00\x00\x00')
    for i in range(len(orig) // 3):
        byteindex = i * 3
        result += b'\xFF' + orig[byteindex:byteindex + 3]
    return bytes(result)

def bannersaga_read(filename, timestamp, data, origin):
    if imagemanip:
        if origin == 'steamcloud' and filename.endswith('png'):
            filename = filename[:-3] + 'img'
            data = PIL.Image.open(io.BytesIO(data))
        if origin == 'icloud' and filename.endswith('bmpzip'):
            filename = filename[:-6] + 'img'
            data = PIL.Image.frombytes('RGB', (480, 360), bannersaga_transform_argb_rgb(zlib.decompress(bytes(data))))
        return ([(filename, timestamp, data)], {})
    else:
        return ([] if (filename.endswith('png') or filename.endswith('bmpzip')) else [(filename, timestamp, data)], {})

def bannersaga_compare(filename, data1, data2):
    if filename.endswith('img'):
        return data1.histogram() == data2.histogram()
    return data1 == data2

def bannersaga_write(filename, data, destination):
    if filename.endswith('img'):
        if destination == 'steamcloud':
            filename = filename[:-3] + 'png'
            pngbytes = io.BytesIO()
            data.save(pngbytes, 'png', optimize=True)
            data = pngbytes.getvalue()
        if destination == 'icloud':
            filename = filename[:-3] + 'bmpzip'
            data = zlib.compress(bannersaga_transform_rgb_argb(data.tobytes()), 9)
    return (filename, data)

# Transistor

def transistor_read(filename, timestamp, data, origin):
    filename = filename[0].lower() + filename[1:]
    return ([(filename, timestamp, data)], {})

def transistor_write(filename, data, destination):
    if destination == 'icloud':
        filename = filename[0].upper() + filename[1:]
    return (filename, data)

# gameobj()

def gameobj(obj):
    if not 'read' in obj:
        obj['read'] = identity_read
    if not 'compare' in obj:
        obj['compare'] = identity_compare
    if not 'write' in obj:
        obj['write'] = identity_write
    if not 'after' in obj:
        obj['after'] = noop_after
    return obj

# Main synchronization function

def sync():
    games = [gameobj({ # The Banner Saga
        'regex': re.compile(r'^[0-4]/(resume|sav_(chapter[1235]|(leaving)?(einartoft|frostvellr)|(dengl|dund|hridvaldy|radormy|skog)r|bjorulf|boersgard|finale|grofheim|hadeborg|ingrid|marek|ridgehorn|sigrholm|stravhs|wyrmtoe))\.(bmpzip|png|save\.json)$'),
        'folder': 'save/saga1',
        'steamcloudid': '237990',
        'icloudid': 'MQ92743Y4D~com~stoicstudio~BannerSaga',
        'read': bannersaga_read,
        'compare': bannersaga_compare,
        'write': bannersaga_write
    }), gameobj({ # Transistor
        'regex': re.compile(r'^[Pp]rofile[1-5]\.sav$'),
        'steamcloudid': '237930',
        'icloudid': 'GPYC69L4CR~iCloud~com~supergiantgames~transistor',
        'icloudfolder': 'Documents',
        'read': transistor_read,
        'write': transistor_write
    })]

    modules = {'steamcloud': None, 'icloud': None}
    modulenum = 0

    for modulename in modules:
        try:
            module = importlib.import_module('.' + modulename, 'airship')
            if module.init():
                modules[modulename] = module
                modulenum += 1
        except ImportError:
            pass

    if modulenum > 1:

        for game in games:
            gamemodules = []
            metadata = {}

            cancontinue = True

            for modulename in modules:
                if modulename + 'id' in game:
                    if modules[modulename] is None:
                        cancontinue = False
                        break
                    else:
                        module = modules[modulename]

                        if modulename + 'folder' in game or 'folder' in game:
                            module.set_folder(game['folder'] if not modulename + 'folder' in game else game[modulename + 'folder'])

                        module.set_id(game[modulename + 'id'])

                        if module.will_work():
                            gamemodules.append(module)
                        else:
                            module.shutdown()
                            cancontinue = False
                            break

            if cancontinue:
                filetimestamps = {}
                filedata = {}
                files = {}
                for moduleindex in range(len(gamemodules)):
                    filenames = gamemodules[moduleindex].get_file_names()
                    if not filenames: # I don't believe you. Maybe you don't have local copies of the files?
                        cancontinue = False
                        break
                    for filename in filenames:
                        if game['regex'].match(filename):
                            readobject = game['read'](filename, gamemodules[moduleindex].get_file_timestamp(filename), gamemodules[moduleindex].read_file(filename), gamemodules[moduleindex].name)
                            metadata.update(readobject[1])
                            for itemfilename, itemfiletimestamp, itemfiledata in readobject[0]:
                                if not itemfilename in filetimestamps:
                                    filetimestamps[itemfilename] = [-1] * len(gamemodules)
                                filetimestamps[itemfilename][moduleindex] = itemfiletimestamp
                                if not itemfilename in filedata:
                                    filedata[itemfilename] = [-1] * len(gamemodules)
                                filedata[itemfilename][moduleindex] = itemfiledata
                if cancontinue:
                    for filename in filetimestamps:
                        for timestamp in filetimestamps[filename]:
                            if timestamp == 0:
                                cancontinue = False
                                break
                        if cancontinue:
                            newerfilesmayexist = True
                            highestlowtimestamp = -1
                            if cancontinue:
                                while newerfilesmayexist:
                                    newerfilesmayexist = False
                                    lowesttimestamp = 2000000000
                                    lowesttimestampindex = -1
                                    for moduleindex in range(len(gamemodules)):
                                        if highestlowtimestamp < filetimestamps[filename][moduleindex] < lowesttimestamp and filetimestamps[filename][moduleindex] > 0:
                                            lowesttimestamp = filetimestamps[filename][moduleindex]
                                            lowesttimestampindex = moduleindex
                                    if lowesttimestampindex != -1:
                                        newerfilesmayexist = True
                                        highestlowtimestamp = lowesttimestamp
                                        for moduleindex in range(len(gamemodules)):
                                            if moduleindex != lowesttimestampindex and filetimestamps[filename][moduleindex] > 0 and game['compare'](filename, filedata[filename][lowesttimestampindex], filedata[filename][moduleindex]):
                                                filetimestamps[filename][moduleindex] = lowesttimestamp

                                highesttimestamp = -1
                                highesttimestampindex = -1
                                for moduleindex in range(len(gamemodules)):
                                    if filetimestamps[filename][moduleindex] > highesttimestamp:
                                        highesttimestamp = filetimestamps[filename][moduleindex]
                                        highesttimestampindex = moduleindex
                                files[filename] = filedata[filename][highesttimestampindex]
                                for moduleindex in range(len(gamemodules)):
                                    if moduleindex != highesttimestampindex and filetimestamps[filename][moduleindex] < highesttimestamp:
                                        writeobject = game['write'](filename, files[filename], gamemodules[moduleindex].name)
                                        gamemodules[moduleindex].write_file(writeobject[0], writeobject[1])
                    game['after'](files, modules, metadata)

            for module in gamemodules:
                module.shutdown()
