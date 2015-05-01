import os
import subprocess
import shutil

os.chdir(os.path.dirname(os.path.abspath(__file__)))

packages = []

for item in os.listdir(os.getcwd()):
    if item.startswith('airship') and os.path.isdir(item):
        packages.append(item)

for package in packages:
    os.chdir(package)
    subprocess.call(['python', 'setup.py', 'bdist_wheel'])
    os.chdir('..')
    for item in os.listdir(package + '/dist'):
        if item.endswith('.whl'):
            if os.path.isfile('dist/' + item):
                os.remove('dist/' + item)
            shutil.move(package + '/dist/' + item, 'dist')
