from __future__ import print_function
import os
import subprocess
import sys

os.chdir(os.path.dirname(os.path.abspath(__file__)))
width = int(subprocess.check_output(['stty', 'size']).split(' ')[1])
timelength = 14
devnull = open(os.devnull, 'w')
force = []
# add specific versions to this array to only benchmark those versions


for item in os.listdir('envs'):

    if os.path.isdir('envs/' + item) and (not force or item in force):
        left = 'Benchmarking in ' + item + ' env:'
        print(left + ' ' * (width - len(left) - timelength) + item + ' ' * (len(item) - timelength))
        subprocessisgood = sys.version_info[0] >= 3 or subprocess.call(['pip', 'show', 'subprocess32'], stdout=devnull, stderr=devnull) == 0
        if not subprocessisgood:
            subprocess.call(['pip', 'install', 'subprocess32'], stdout=devnull, stderr=devnull)
        subprocess.call([sys.executable, 'benchmark.py', item, str(width), str(timelength)])
