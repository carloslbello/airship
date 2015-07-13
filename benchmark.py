from __future__ import division
import time
import os
import subprocess
import itertools

"""Used to test how long it takes to run Airship with various optional
   packages installed; first activate a virtualenv created by make-envs.py,
   then do `python benchmark.py`"""

devnull = open(os.devnull, 'w')
boolean = [False, True]

def benchmark(command):
    clock = time.time()
    subprocess.call(command)
    return time.time() - clock

def benchmark_multiple(command, times):
    subprocess.call(command)
    sum = 0
    num = 0
    while num < times:
        sum += benchmark(command)
        num += 1
    return sum / times

results = []
optionals = ['pillow', 'scandir']

for permutation in itertools.product(boolean, boolean):
    packages = {}

    for index in range(len(optionals)):
        packages[optionals[index]] = permutation[index]

    packagestr = ''

    for package in packages:
        packageinstalled = subprocess.call(['pip', 'show', package], stdout=devnull, stderr=devnull) == 0
        if packageinstalled and not packages[package]:
            subprocess.call(['pip', 'uninstall', '-y', package])
        if not packageinstalled and packages[package]:
            subprocess.call(['pip', 'install', package])

        if packages[package]:
            if not packagestr:
                packagestr = ' ('
            else:
                packagestr += ', '
            packagestr += package

    if packagestr:
        packagestr += ')'

    subprocess.call(['python', 'test.py'])
    results.append('Time' + packagestr + ': ' + str(benchmark_multiple(['python', 'test/run.py'], 10)))

for result in results:
    print(result)
