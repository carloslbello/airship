import os
import importlib
import re
import time

def sync():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    games = [{ # The Banner Saga
        'regex': '[0-4]/(resume|sav_(chapter[1235]|(leaving)?(einartoft|frostvellr)|(dengl|dund|hridvaldy|radormy|skog)r|bjorulf|boersgard|finale|grofheim|hadeborg|ingrid|marek|ridgehorn|sigrholm|stravhs|wyrmtoe))\.save\.json',
        'folder': 'save/saga1',
        'steamcloudid': '237990',
        'icloudid': 'MQ92743Y4D~com~stoicstudio~BannerSaga'
    }]

    modules = {'steamcloud': None, 'icloud': None}
    modulenum = 0

    for modulename in modules:
        try:
            module = importlib.import_module('.' + modulename, 'airship')
            if module.init():
                modules[modulename] = module
                modulenum += 1
        except:
            pass

    if modulenum > 1:

        for game in games:
            gamemodules = []

            for modulename in modules:
                if modules[modulename] is not None and modulename + 'id' in game:
                    module = modules[modulename]

                    if modulename + 'folder' in game or 'folder' in game:
                        module.set_folder(game['folder'] if not modulename + 'folder' in game else game[modulename + 'folder'])

                    module.set_id(game[modulename + 'id'])

                    if module.will_work():
                        gamemodules.append(module)
                    else:
                        module.shutdown()

            if len(gamemodules) > 1:
                filetimestamps = {}
                for moduleindex in range(len(gamemodules)):
                    filenames = gamemodules[moduleindex].get_file_names()
                    for filename in filenames:
                        if re.match(game['regex'], filename):
                            if not filename in filetimestamps:
                                filetimestamps[filename] = [0] * len(gamemodules)
                            filetimestamps[filename][moduleindex] = gamemodules[moduleindex].get_file_timestamp(filename)

                for filename in filetimestamps:
                    newerfilesmayexist = True
                    highestlowtimestamp = -1
                    while newerfilesmayexist:
                        newerfilesmayexist = False
                        lowesttimestamp = int(time.time())
                        lowesttimestampindex = -1
                        for moduleindex in range(len(gamemodules)):
                            if highestlowtimestamp < filetimestamps[filename][moduleindex] < lowesttimestamp and filetimestamps[filename][moduleindex] > 0:
                                lowesttimestamp = filetimestamps[filename][moduleindex]
                                lowesttimestampindex = moduleindex
                        if lowesttimestampindex != -1:
                            newerfilesmayexist = True
                            highestlowtimestamp = lowesttimestamp
                            originaldata = gamemodules[lowesttimestampindex].read_file(filename)
                            if originaldata is not None:
                                for moduleindex in range(len(gamemodules)):
                                    if moduleindex != lowesttimestampindex and filetimestamps[filename][moduleindex] > 0 and gamemodules[moduleindex].read_file(filename) == originaldata:
                                        filetimestamps[filename][moduleindex] = lowesttimestamp

                    highesttimestamp = -1
                    highesttimestampindex = -1
                    for moduleindex in range(len(gamemodules)):
                        if filetimestamps[filename][moduleindex] > highesttimestamp:
                            highesttimestamp = filetimestamps[filename][moduleindex]
                            highesttimestampindex = moduleindex
                    highesttimestampdata = gamemodules[highesttimestampindex].read_file(filename)
                    if highesttimestampdata is not None:
                        for moduleindex in range(len(gamemodules)):
                            if moduleindex != highesttimestampindex and filetimestamps[filename][moduleindex] < highesttimestamp:
                                gamemodules[moduleindex].write_file(filename, highesttimestampdata)

            for module in gamemodules:
                module.shutdown()
