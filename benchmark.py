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
numtimes = 5
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

def get_python_ver(python):
    if python.startswith('python'):
        name = 'CPython'
    elif python.startswith('pypy'):
        name = 'PyPy'
    else:
        name = python[0].upper() + python[1:]

    vflag = subprocess.Popen([python, '-V'], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[1 if not (python.startswith('python3.4') or python.startswith('python3.5')) else 0][:-1]
    index = vflag.find(name) + len(name) + 1
    if python.startswith('pypy3'):
        name = 'PyPy3'
    spaceindex = vflag.find(' ', index)
    if spaceindex == -1:
        ver = vflag[index:]
    else:
        ver = vflag[index:spaceindex]
    return name + ' ' + ver

results = []
failedinstalls = []
optionals = ['pillow', 'scandir']
applicableoptionals = ['pillow']


execfile('envs/' + item + '/bin/activate_this.py', dict(__file__='envs/' + item + '/bin/activate_this.py'))

if subprocess.call(['python', '-c', 'import os;exit(not hasattr(os,\'scandir\'))']) != 0:
    applicableoptionals.append('scandir')

basetime = 0

optionalsets = []

for permutation in itertools.product(*boolean * len(optionals)):
    optset = []
    for index in range(len(permutation)):
        if permutation[index]:
            optset.append(optionals[index])
    optionalsets.append(optset)

line = get_python_ver(item) + ','

for optset in optionalsets:
    packages = {}
    for package in optionals:
        packages[package] = False
    candothething = True
    for package in optset:
        if not package in applicableoptionals:
            candothething = False
            line += 'N/A,'
            break
        packages[package] = True

    if candothething:
        for package in packages:
            packageinstalled = subprocess.call(['pip', 'show', package], stdout=devnull, stderr=devnull) == 0
            prevfailedinstall = package in failedinstalls
            if packageinstalled and not packages[package]:
                subprocess.call(['pip', 'uninstall', '-y', package], stdout=devnull, stderr=devnull)
            if not packageinstalled and packages[package]:
                if not prevfailedinstall:
                    try:
                        failedinstall = subprocess.call(['pip', 'install', package], stdout=devnull, stderr=devnull, timeout=30) != 0
                    except subprocess.TimeoutExpired:
                        failedinstall = True
                if failedinstall or prevfailedinstall:
                    if not prevfailedinstall:
                        failedinstalls.append(package)
                    subprocess.call(['pip', 'uninstall', '-y', package], stdout=devnull, stderr=devnull)
                    candothething = False
                    line += 'N/A,'
                    break

        if candothething:
            line += str(benchmark_multiple(['python', 'test/run.py'], numtimes)) + ','

with open('bench.csv', 'a') as bench:
    bench.write(line[:-1] + '\n')
