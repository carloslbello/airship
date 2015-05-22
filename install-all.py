import os
import subprocess

"""Used to test functionality in virtual environments created by virtualenv
   You must first activate the desired environment"""

directory = os.path.dirname(os.path.abspath(__file__))

packages = []

for item in os.listdir(os.getcwd()):
    if item.startswith('airship') and os.path.isdir(item):
        packages.append(item)

for package in packages:
    subprocess.call(['pip', 'install', '-U', directory + '/' + package])
