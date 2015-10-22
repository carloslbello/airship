import os
import re
import subprocess
import shutil
import requests
from distutils.version import LooseVersion

"""Used to make wheels to upload to PyPI"""

os.chdir(os.path.dirname(os.path.abspath(__file__)))

packages = []
binaryfolders = {'bin_win32': 'win32', 'bin_win64': 'win64', 'bin_osx': 'macosx_10_6_universal'} #, 'bin_lnx32': 'linux_i686', 'bin_lnx64': 'linux_x86_64'}

packagedataregex = re.compile(r'^\s+\'airship\':\s+\[(.+)\]$', flags=re.MULTILINE)
packageversionregex = re.compile(r'^\s+version=\'([^\']+)\',$', flags=re.MULTILINE)

for item in os.listdir('.'):
    if item.startswith('airship') and os.path.isdir(item):
        with open(item + '/setup.py') as setupfile:
            if LooseVersion(packageversionregex.search(setupfile.read()).groups()[0]) > LooseVersion(requests.get('http://pypi.python.org/pypi/' + item.replace('.', '-') + '/json').json()['info']['version']):
                packages.append(item)

if not os.path.isdir('dist'):
    os.mkdir('dist')

for package in packages:
    os.chdir(package)
    for item in os.listdir('.'):
        if os.path.isdir(item) and item != 'airship' and item != 'dist':
            shutil.rmtree(item)
    with open('setup.py') as setupfile:
        setupfilecontents = setupfile.read()
    match = packagedataregex.search(setupfilecontents)
    if match:
        replace = '[' + match.groups(1)[0] + ']'
        packagedata = match.groups(1)[0].replace('\'', '').replace(',', '').split()
        for binaryfolder in binaryfolders:
            filestoinclude = []
            for filename in packagedata:
                if filename.startswith(binaryfolder):
                    filestoinclude.append(filename)
            if filestoinclude:
                with open('setup.py', 'w') as setupfile:
                    setupfile.write(setupfilecontents.replace(replace, str(filestoinclude)))
                subprocess.call(['python', 'setup.py', 'bdist_wheel', '--universal'])
                for item in os.listdir('.'):
                    if os.path.isdir(item) and item != 'airship' and item != 'dist':
                        shutil.rmtree(item)
                for item in os.listdir('dist'):
                    if 'any' in item:
                        os.rename('dist/' + item, 'dist/' + item.replace('any', binaryfolders[binaryfolder]))
                        break
        with open('setup.py', 'w') as setupfile:
            setupfile.write(setupfilecontents)
    subprocess.call(['python', 'setup.py', 'bdist_wheel', '--universal'])
    os.chdir('..')
    for item in os.listdir(package + '/dist'):
        if item.endswith('.whl'):
            shutil.move(package + '/dist/' + item, 'dist')
