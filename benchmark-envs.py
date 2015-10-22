import os
import subprocess
import sys
import itertools

os.chdir(os.path.dirname(os.path.abspath(__file__)))
devnull = open(os.devnull, 'w')
force = []
# add specific versions to this array to only benchmark those versions

boolean = [[False, True]]

optionalsets = []
optionals = ['pillow', 'scandir']

for permutation in itertools.product(*boolean * len(optionals)):
    optset = []
    for index in range(len(permutation)):
        if permutation[index]:
            optset.append(optionals[index])
    optionalsets.append(optset)

top = 'Interpreter,'
for optset in optionalsets:
    if not optset:
        top += 'No optional packages,'
    else:
        top += ' + '.join(optset) + ','

with open('bench.csv', 'w') as bench:
    bench.write(top[:-1] + '\n')

subprocessisgood = sys.version_info[0] >= 3 or subprocess.call(['pip', 'show', 'subprocess32'], stdout=devnull, stderr=devnull) == 0
if not subprocessisgood:
    subprocess.call(['pip', 'install', 'subprocess32'], stdout=devnull, stderr=devnull)

for item in os.listdir('envs'):
    if os.path.isdir('envs/' + item) and (not force or item in force):
        subprocess.call([sys.executable, 'benchmark.py', item])
