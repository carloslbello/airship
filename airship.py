import os
import subprocess

games = []

void = open(os.devnull, 'w')

for game in games:
    icloudFolder = os.path.expanduser('~/Library/Mobile Documents/' + \
                   game['icloudbundleid'] + '/' + game['folder'])

    if not os.path.isdir(icloudFolder):
        os.path.makedirs(icloudFolder)

    subprocess.call(['python', 'propeller.py', game['steamappid'], \
                     game['icloudbundleid'], game['folder'], game['regex']], \
                     stdout = void, stderr = void)
