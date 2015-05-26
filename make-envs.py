import os
import subprocess

directory = os.path.dirname(os.path.abspath(__file__))

devnull = open(os.devnull, 'w')

if not os.path.isdir(directory + '/envs'):
    os.mkdir(directory + '/envs')

pythons = [('Python 2.6', 'python2.6'), ('Python 2.7', 'python2.7'), ('Python 3.2', 'python3.2'), ('Python 3.3', 'python3.3'), ('Python 3.4', 'python3.4'), ('Python 3.5', 'python3.5'), ('PyPy', 'pypy')]

for python in pythons:
    if subprocess.call(['which', python[1]], stdout=devnull, stderr=devnull) != 0:
        print('Couldn\'t find ' + python[0] + ', not making env')
    else:
        path = subprocess.check_output(['which', python[1]])[:-1]
        subprocess.call(['virtualenv', '-p', path, directory + '/envs/' + python[1]])
