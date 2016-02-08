import re

# Defined as a boolean if a function that can use it is run

imagemanip = None

modules = []

try:
    import icloud
    modules.append(icloud)
except ImportError:
    pass

try:
    import steamcloud
    modules.append(steamcloud)
except ImportError:
    pass

# Module name cleaner


def modulename(name):
    dotindex = name.rfind('.')
    if dotindex != -1:
        name = name[dotindex + 1:]
    return name

# Data manipulation functions

# Identity


def identity_read(filename, timestamp, data, origin, regexes):
    return ([(filename, timestamp, data)], {})


def identity_compare(filename, data1, data2):
    return data1 == data2


def identity_write(filename, data, destination, meta, regexes):
    return (filename, data)


def noop_after(filedata, modules, metadata):
    pass

# The Banner Saga


def bannersaga_transform_argb_rgb(orig):
    result = bytearray()
    orig = orig[13:]
    for i in range(0, len(orig), 4):
        result += orig[i + 1:i + 4]
    return bytes(result)


def bannersaga_transform_rgb_argb(orig):
    result = bytearray(b'\x00\x00\x01\xe0\x00\x00\x01h\x00\x00\x00\x00\x00')
    for i in range(0, len(orig), 3):
        result += b'\xFF' + orig[i:i + 3]
    return bytes(result)


def bannersaga_read_func():
    global imagemanip
    if imagemanip is None:
        try:
            import PIL.Image
            imagemanip = True
        except ImportError:
            imagemanip = False
    return (bannersaga_read_imagemanip
            if imagemanip else bannersaga_read_noimagemanip)


def bannersaga_read_imagemanip(filename, timestamp, data, origin, regexes):
    import PIL.Image
    if origin == 'steamcloud' and filename.endswith('png'):
        import io
        filename = filename[:-3] + 'img'
        data = PIL.Image.open(io.BytesIO(data))
    if origin == 'icloud' and filename.endswith('bmpzip'):
        import zlib
        filename = filename[:-6] + 'img'
        data = PIL.Image.frombytes('RGB', (480, 360),
                                   bannersaga_transform_argb_rgb(
                                        zlib.decompress(bytes(data))))
    return ([(filename, timestamp, data)], {})


def bannersaga_read_noimagemanip(filename, timestamp, data, origin, regexes):
    return ([] if (filename.endswith('png') or filename.endswith('bmpzip'))
            else [(filename, timestamp, data)], {})


def bannersaga_compare(filename, data1, data2):
    if filename.endswith('img'):
        return data1.tobytes() == data2.tobytes()
    return data1 == data2


def bannersaga_write(filename, data, destination, meta, regexes):
    if filename.endswith('img'):
        if destination == 'steamcloud':
            import io
            filename = filename[:-3] + 'png'
            pngbytes = io.BytesIO()
            data.save(pngbytes, 'png', optimize=True)
            data = pngbytes.getvalue()
        if destination == 'icloud':
            import zlib
            filename = filename[:-3] + 'bmpzip'
            data = zlib.compress(bannersaga_transform_rgb_argb(data.tobytes()),
                                 9)
    return (filename, data)

# Transistor


def transistor_read(filename, timestamp, data, origin, regexes):
    return ([(filename.lower(), timestamp, data)], {})


def transistor_write(filename, data, destination, meta, regexes):
    if destination == 'icloud':
        filename = filename[0].upper() + filename[1:]
    return (filename, data)

# Costume Quest


def costumequest_read(filename, timestamp, data, origin, regexes):
    meta = {}
    timeplayedregex = regexes['timeplayed']
    if origin == 'icloud':
        match = timeplayedregex.match(data).groups()
        meta[filename] = match[1]
        data = (data[:4] + b'\x0b' + data[5:].replace(b'_mobile', b'')
                                             .replace(match[0], b''))
    return ([(filename, timestamp, data)], meta)


def costumequest_write(filename, data, destination, meta, regexes):
    if destination == 'icloud':
        semicolonafterplacementsindex = data.find(b';',
                                                  data.find(
                                                    b'DestroyedPlacements'))
        if semicolonafterplacementsindex == -1:
            semicolonafterplacementsindex = len(data)
        data = regexes['level'].sub(b'worlds/\\1_mobile/\\1_mobile',
                                    data[:4] + b'\x0c' +
                                    data[5:semicolonafterplacementsindex] +
                                    b';TimePlayed=' +
                                    (b'0' if filename not in meta else
                                     meta[filename]) +
                                    data[semicolonafterplacementsindex:])
    return (filename, data)

# Race the Sun


def racethesun_read(filename, timestamp, data, origin, regexes):
    return ([('savegame.xml', timestamp, data)], {})


def racethesun_write(filename, data, destination, meta, regexes):
    return ('rts_save.xml' if destination == 'icloud'
            else 'savegame.xml', data)

# gameobj()


def gameobj(obj):
    if 'read' not in obj:
        obj['read'] = identity_read
    if 'compare' not in obj:
        obj['compare'] = identity_compare
    if 'write' not in obj:
        obj['write'] = identity_write
    if 'after' not in obj:
        obj['after'] = noop_after
    return obj

# Main synchronization function


def sync():
    games = [gameobj({  # The Banner Saga
        'regexformats': {
            'base': (r'^[0-4]/(resume|sav_(chapter[1235]|(leaving)?(einartof' +
                     r't|frostvellr)|(dengl|dund|hridvaldy|radormy|skog)r|bj' +
                     r'orulf|boersgard|finale|grofheim|hadeborg|ingrid|marek' +
                     r'|ridgehorn|sigrholm|stravhs|wyrmtoe))\.(bmpzip|png|sa' +
                     r've\.json)$')
        },
        'folder': 'save/saga1',
        'modules': {
            'steamcloud': {
                'id': '237990'
            },
            'icloud': {
                'id': 'MQ92743Y4D~com~stoicstudio~BannerSaga'
            }
        },
        'read': bannersaga_read_func(),
        'compare': bannersaga_compare,
        'write': bannersaga_write
    }), gameobj({  # Transistor
        'regexformats': {
            'base': r'^[Pp]rofile[1-5]\.sav$'
        },
        'modules': {
            'steamcloud': {
                'id': '237930'
            },
            'icloud': {
                'id': 'GPYC69L4CR~iCloud~com~supergiantgames~transistor',
                'folder': 'Documents',
            }
        },
        'read': transistor_read,
        'write': transistor_write
    }), gameobj({  # Costume Quest
        'regexformats': {
            'base': r'^CQ(_DLC)?_save_[012]$',
            'timeplayed': r'^.+(;TimePlayed=([1-9]*[0-9](\.[0-9]+)?)).*$',
            'level': r'worlds\/([a-z_]+)\/\1'
        },
        'modules': {
            'steamcloud': {
                'id': '115100'
            },
            'icloud': {
                'id': '8VM2L59D89~com~doublefine~cqios',
                'folder': 'Documents'
            }
        },
        'read': costumequest_read,
        'write': costumequest_write
    }), gameobj({  # Race the Sun
        'regexformats': {
            'base': r'^(savegame|rts_save)\.xml$'
        },
        'modules': {
            'steamcloud': {
                'id': '253030'
            },
            'icloud': {
                'id': 'iCloud~com~flippfly~racethesun',
                'folder': 'Documents'
            }
        },
        'read': racethesun_read,
        'write': racethesun_write
    })]

    if len(modules) > 1:

        workingmodules = {}
        modulenum = 0

        for module in modules:
            if module.init():
                workingmodules[modulename(module.__name__)] = module
                modulenum += 1

        if modulenum > 1:

            for game in games:
                gamemodules = []
                metadata = {}
                cancontinue = True

                for module in modules:
                    name = modulename(module.__name__)
                    if name in game['modules']:
                        if name not in workingmodules:
                            cancontinue = False
                            break
                        else:
                            module = workingmodules[name]

                            if ('folder' in game['modules'][name] or
                                    'folder' in game):
                                module.set_folder(game['folder']
                                                  if 'folder' not in
                                                  game['modules'][name] else
                                                  game['modules'][name]
                                                                 ['folder'])

                            module.set_id(game['modules'][name]['id'])

                            if module.will_work():
                                gamemodules.append(module)
                            else:
                                module.shutdown()
                                cancontinue = False
                                break

                if cancontinue:
                    regexes = {}
                    filetimestamps = {}
                    filedata = {}
                    files = {}
                    for regex in game['regexformats']:
                        if regex == 'base':
                            fileregex = re.compile(game['regexformats']
                                                       ['base'])
                        else:
                            regexes[regex] = re.compile(game['regexformats']
                                                            [regex])
                    for moduleindex in range(len(gamemodules)):
                        cancontinue = False
                        for filename in (gamemodules[moduleindex]
                                         .get_file_names()):
                            if fileregex.match(filename):
                                readobject = (game['read']
                                              (filename,
                                               gamemodules[moduleindex]
                                               .get_file_timestamp(filename),
                                               gamemodules[moduleindex]
                                               .read_file(filename),
                                               modulename(
                                                 gamemodules[moduleindex]
                                                 .__name__), regexes))
                                metadata.update(readobject[1])
                                for (itemfilename, itemfiletimestamp,
                                        itemfiledata) in readobject[0]:
                                    if itemfilename not in filetimestamps:
                                        filetimestamps[itemfilename] = \
                                            [-1] * len(gamemodules)
                                    (filetimestamps[itemfilename]
                                        [moduleindex]) = itemfiletimestamp
                                    if itemfilename not in filedata:
                                        filedata[itemfilename] = \
                                            [-1] * len(gamemodules)
                                    filedata[itemfilename][moduleindex] = \
                                        itemfiledata
                                cancontinue = True
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
                                        for moduleindex in \
                                                range(len(gamemodules)):
                                            if (highestlowtimestamp <
                                                filetimestamps[filename]
                                                              [moduleindex] <
                                                lowesttimestamp and
                                                filetimestamps[filename]
                                                              [moduleindex] >
                                                    0):
                                                lowesttimestamp = \
                                                    (filetimestamps[filename]
                                                        [moduleindex])
                                                lowesttimestampindex = \
                                                    moduleindex
                                        if lowesttimestampindex != -1:
                                            newerfilesmayexist = True
                                            highestlowtimestamp = \
                                                lowesttimestamp
                                            for moduleindex in \
                                                    range(len(gamemodules)):
                                                if (moduleindex !=
                                                    lowesttimestampindex and
                                                    filetimestamps[filename]
                                                        [moduleindex] > 0 and
                                                    game['compare']
                                                    (filename,
                                                     filedata[filename]
                                                        [lowesttimestampindex],
                                                     filedata[filename]
                                                        [moduleindex])):
                                                    (filetimestamps[filename]
                                                        [moduleindex]) = \
                                                        lowesttimestamp

                                    highesttimestamp = -1
                                    highesttimestampindex = -1
                                    for moduleindex in range(len(gamemodules)):
                                        if (filetimestamps[filename]
                                                [moduleindex] >
                                                highesttimestamp):
                                            highesttimestamp = \
                                                (filetimestamps
                                                    [filename][moduleindex])
                                            highesttimestampindex = moduleindex
                                    files[filename] = \
                                        (filedata[filename]
                                         [highesttimestampindex])
                                    for moduleindex in range(len(gamemodules)):
                                        if (moduleindex !=
                                            highesttimestampindex and
                                            filetimestamps[filename]
                                            [moduleindex] <
                                                highesttimestamp):
                                            writeobject = (game['write']
                                                           (filename,
                                                            files[filename],
                                                            modulename(
                                                                gamemodules
                                                                [moduleindex]
                                                                .__name__),
                                                            metadata, regexes))
                                            (gamemodules[moduleindex]
                                                .write_file(*writeobject))
                        game['after'](files, modules, metadata)
                for module in gamemodules:
                    module.shutdown()
