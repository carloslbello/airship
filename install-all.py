import os
import shutil
import subprocess

"""Used to test functionality in virtual environments created by virtualenv
   You must first activate the desired environment and run get-bin.sh"""

directory = os.path.dirname(os.path.abspath(__file__))

packages = []

for item in os.listdir(directory):
    if item.startswith('airship') and os.path.isdir(item):
        packages.append('./' + item)

subprocess.call(['pip', 'install', '-U', '--force-reinstall', '--no-index',
                 '--no-deps'] + packages)
