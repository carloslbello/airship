import os
import sys
import subprocess

os.chdir(os.path.dirname(os.path.abspath(__file__)))

games = [{ # The Banner Saga
    'regex': '[0-4]/(resume|sav_(chapter[1235]|(leaving)?(einartoft|frostvellr)|(dengl|dund|hridvaldy|radormy|skog)r|bjorulf|boersgard|finale|grofheim|hadeborg|ingrid|marek|ridgehorn|sigrholm|stravhs|wyrmtoe))\.save\.json',
    'folder': 'save/saga1',
    'steamcloudid': '237990',
    'icloudid': 'MQ92743Y4D~com~stoicstudio~BannerSaga'
}]

void = open(os.devnull, 'w')

for game in games:
    arguments = ['python', 'propeller.py']

    for property in game:
        arguments.append('--' + property)
        arguments.append(game[property])

    subprocess.call(arguments, stdout=void, stderr=void)
