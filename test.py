import os
import shutil

"""Used to test new functionality without installing any packages
   To test, run this script, then run test/run.py"""

directory = os.path.dirname(os.path.abspath(__file__))

packages = []
binaryfolders = ['bin_win32', 'bin_win64', 'bin_osx', 'bin_lnx32', 'bin_lnx64']

if os.path.isdir(directory + '/test'):
    shutil.rmtree(directory + '/test')

for folder in binaryfolders:
    os.makedirs(directory + '/test/' + folder)

shutil.copy(directory + '/run.py', 'test')

for item in os.listdir(directory):
    if item.startswith('airship') and os.path.isdir(item):
        packages.append(item)

for package in packages:
    items = os.listdir(directory + '/' + package + '/airship')
    for item in items:
        if item.endswith('.py'):
            shutil.copy(directory + '/' + package + '/airship/' + item, 'test')
    for binaryfolder in list(set(binaryfolders) & set(items)):
        for item in os.listdir(os.getcwd() + '/' + package + '/airship/' +
                               binaryfolder):
            if not item.startswith('.'):
                shutil.copy(directory + '/' + package + '/airship/' +
                            binaryfolder + '/' + item,
                            directory + '/test/' + binaryfolder)
