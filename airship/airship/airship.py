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
                cancontinue = True
                for moduleindex in xrange(len(gamemodules)):
                    filenames = gamemodules[moduleindex].get_file_names()
                    if not filenames: # I don't believe you. Maybe you don't have local copies of the files?
                        cancontinue = False
                        break
                    for filename in filenames:
                        if re.match(game['regex'], filename):
                            if not filename in filetimestamps:
                                filetimestamps[filename] = [-1] * len(gamemodules)
                            filetimestamps[filename][moduleindex] = gamemodules[moduleindex].get_file_timestamp(filename)
                if cancontinue:
                    for filename in filetimestamps:
                        for timestamp in filetimestamps[filename]:
                            if timestamp == 0:
                                cancontinue = False
                                break
                        if cancontinue:
                            newerfilesmayexist = True
                            highestlowtimestamp = -1
                            filedata = [None] * len(gamemodules)
                            for moduleindex in range(len(gamemodules)):
                                if filetimestamps[filename][moduleindex] != -1:
                                    filedata[moduleindex] = gamemodules[moduleindex].read_file(filename)
                            for dataindex in xrange(len(filedata)):
                                if filedata[dataindex] is None and filetimestamps[filename][dataindex] != -1:
                                    cancontinue = False
                                    break
                            if cancontinue:
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
                                        originaldata = filedata[lowesttimestampindex]
                                        if originaldata is not None:
                                            for moduleindex in range(len(gamemodules)):
                                                if moduleindex != lowesttimestampindex and filetimestamps[filename][moduleindex] > 0 and filedata[moduleindex] == originaldata:
                                                    filetimestamps[filename][moduleindex] = lowesttimestamp

                                highesttimestamp = -1
                                highesttimestampindex = -1
                                for moduleindex in range(len(gamemodules)):
                                    if filetimestamps[filename][moduleindex] > highesttimestamp:
                                        highesttimestamp = filetimestamps[filename][moduleindex]
                                        highesttimestampindex = moduleindex
                                highesttimestampdata = filedata[highesttimestampindex]
                                if highesttimestampdata is not None:
                                    for moduleindex in range(len(gamemodules)):
                                        if moduleindex != highesttimestampindex and filetimestamps[filename][moduleindex] < highesttimestamp:
                                            gamemodules[moduleindex].write_file(filename, highesttimestampdata)

            for module in gamemodules:
                module.shutdown()
