import os
import re
import subprocess
import shutil
import requests
from distutils.version import LooseVersion

"""Used to make wheels to upload to PyPI"""

os.chdir(os.path.dirname(os.path.abspath(__file__)))

packages = ['airship', 'airship.steamcloud', 'airship.icloud']
binaryfolders = {'bin_win32': 'win32', 'bin_win64': 'win64',
                 'bin_osx': 'macosx'}
linuxbinaryfolders = {'bin_lnx32': 'linux_i686', 'bin_lnx64': 'linux_x86_64'}

dataarrayregex = re.compile(r'\'airship\'\s*:\s*\[(.*?)\]',
                            flags=re.DOTALL)
stringregex = re.compile(r'(\'(?:[^\'\\]|\\.)*\'|\"(?:[^\"\\]|\\.)*\")')
versionregex = re.compile(r'^\s+version=\'([^\']+)\',$', flags=re.M)

if not packages:
    for item in os.listdir('.'):
        if item.startswith('airship') and os.path.isdir(item):
            with open(item + '/setup.py') as setupfile:
                localver = versionregex.search(setupfile.read()).groups()[0]
                pypiver = (requests.get('http://pypi.python.org/pypi/' +
                                        item.replace('.', '-') + '/json')
                                   .json()['info']['version'])
                if LooseVersion(localver) > LooseVersion(pypiver):
                    packages.append(item)

if not os.path.isdir('dist'):
    os.mkdir('dist')

for package in packages:
    tags = {'macosx': 'macosx_10_0_universal'}
    os.chdir(package)
    for item in os.listdir('.'):
        if os.path.isdir(item) and item != 'airship' and item != 'dist':
            shutil.rmtree(item)
    with open('setup.py') as setupfile:
        setupfilecontents = setupfile.read()
    for line in setupfilecontents.split('\n'):
        if line.startswith('# @'):
            equals = line.find('=')
            tags[line[3:equals]] = line[equals + 1:].rstrip()
    match = dataarrayregex.search(setupfilecontents)
    if match:
        replace = match.groups(1)[0]
        packagedata = stringregex.findall(replace)
        replace = '[' + replace + ']'
        for binaryfolder in binaryfolders:
            tag = binaryfolders[binaryfolder]
            filestoinclude = []
            for filename in packagedata:
                filename = filename[1:-1]
                if filename.startswith(binaryfolder):
                    filestoinclude.append(filename)

            if filestoinclude:
                with open('setup.py', 'w') as setupfile:
                    setupfile.write(
                        setupfilecontents.replace(replace, str(filestoinclude))
                    )
                subprocess.call(['python', 'setup.py', 'bdist_wheel',
                                 '--universal'])
                for item in os.listdir('.'):
                    if (os.path.isdir(item) and item != 'airship' and
                            item != 'dist'):
                        shutil.rmtree(item)
                for item in os.listdir('dist'):
                    if 'any' in item:
                        realtag = tag if tag not in tags else tags[tag]
                        os.rename('dist/' + item, 'dist/' +
                                  item.replace('any', realtag))
                        break
        with open('setup.py', 'w') as setupfile:
            setupfile.write(setupfilecontents)
    subprocess.call(['python', 'setup.py', 'bdist_wheel', '--universal'])
    if 'any' in tags:
        for item in os.listdir('dist'):
            if 'any' in item:
                os.rename('dist/' + item, 'dist/' +
                          item.replace('any', tags['any']))
                break

    os.chdir('..')
    for item in os.listdir(package + '/dist'):
        if item.endswith('.whl'):
            shutil.move(package + '/dist/' + item, 'dist')
    for item in os.listdir(package):
        if os.path.isdir(package + '/' + item) and item != 'airship':
            shutil.rmtree(package + '/' + item)
