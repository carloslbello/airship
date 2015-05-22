import os
import subprocess
import shutil

"""Used to make wheels to upload to PyPI"""

os.chdir(os.path.dirname(os.path.abspath(__file__)))

packages = []

for item in os.listdir(os.getcwd()):
    if item.startswith('airship') and os.path.isdir(item):
        packages.append(item)

if os.path.isdir('dist'):
    for item in os.listdir('dist'):
        os.remove('dist/' + item)
else:
    os.mkdir('dist')

for package in packages:
    os.chdir(package)
    subprocess.call(['python', 'setup.py', 'bdist_wheel', '--universal'])
    os.chdir('..')
    for item in os.listdir(package + '/dist'):
        if item.endswith('.whl'):
            shutil.move(package + '/dist/' + item, 'dist')
