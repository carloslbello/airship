from __future__ import division, print_function
import time
import sys
import os
import itertools
import sys
import subprocess32 as subprocess

"""Used to test how long it takes to run Airship with various optional
   packages installed; `python benchmark.py env_name`

   Requires package subprocess32 and Python 2.x"""

devnull = open(os.devnull, 'w')
boolean = [[False, True]]
terminalwidth = int(sys.argv[2])
numtimes = 2
item = sys.argv[1]

def benchmark(command):
    clock = time.time()
    subprocess.call(command, stdout=devnull, stderr=devnull)
    return time.time() - clock

def benchmark_multiple(command, times):
    subprocess.call(command, stdout=devnull, stderr=devnull)
    prod = 1
    num = 0
    while num < times:
        prod *= benchmark(command)
        num += 1
    return prod ** (1.0/times)

results = []
failedinstalls = []
optionals = ['pillow']

execfile('envs/' + item + '/bin/activate_this.py', dict(__file__='envs/' + item + '/bin/activate_this.py'))

if subprocess.call(['python', '-c', 'import os;exit(not hasattr(os,\'scandir\'))']) != 0:
    optionals.append('scandir')

basetime = 0

for permutation in itertools.product(*boolean * len(optionals)):
    packages = {}

    for index in range(len(optionals)):
        packages[optionals[index]] = permutation[index]

    packagestr = ''
    candothething = True
    installedpackages = []

    for package in packages:
        packageinstalled = subprocess.call(['pip', 'show', package], stdout=devnull, stderr=devnull) == 0
        prevfailedinstall = package in failedinstalls
        if packageinstalled and not packages[package]:
            subprocess.call(['pip', 'uninstall', '-y', package], stdout=devnull, stderr=devnull)
        if not packageinstalled and packages[package]:
            try:
                failedinstall = subprocess.call(['pip', 'install', package], stdout=devnull, stderr=devnull, timeout=30) != 0
            except subprocess.TimeoutExpired:
                failedinstall = True
            if failedinstall or prevfailedinstall:
                if not prevfailedinstall:
                    failedinstalls.append(package)
                subprocess.call(['pip', 'uninstall', '-y', package], stdout=devnull, stderr=devnull)
                candothething = False
        if packages[package]:
            installedpackages.append(package)

    packagestr = ''
    if installedpackages:
        packagestr = ' (' + ', '.join(installedpackages) + ')'

    if candothething:
        subprocess.call(['python', 'test.py'])
        left = 'G-mean time of ' + str(numtimes) + packagestr + ':'
        result = benchmark_multiple(['python', 'test/run.py'], numtimes)
        if not installedpackages:
            basetime = result
        difference = result - basetime
        sign = ''
        if difference == 0:
            sign = u'\u00b1'
        if difference > 0:
            sign = '+'
        right = '%.4f' % result + ' ' + sign + '%.4f' % difference
        print(left + ' ' * (terminalwidth - len(left) - 14) + right)

if failedinstalls:
    failed = 'Package' + ('s' if len(failedinstalls) > 1 else '') + ' ' + ', '.join(failedinstalls) + ' failed to install and w' + ('ere' if len(failedinstalls) > 1 else 'as') + ' not used'
    print(failed + ' ' * (terminalwidth - len(failed) - 14) + u'0.0000 \u00b10.0000')
