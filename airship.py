import os
import subprocess

games = []

void = open(os.devnull, 'w')

for game in games:
    arguments = ['python', 'propeller.py']

    for property in game:
        arguments.append('--' + property)
        arguments.append(game[property])

    subprocess.call(arguments, stdout = void, stderr = void)
