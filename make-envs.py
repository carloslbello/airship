from __future__ import print_function
import os
import subprocess
import shutil

"""Creates virtual environments for installed Python interpreters.
   Requires valid python2 and python3 installations for respective
   interpreters' environments (based on major version)"""

directory = os.path.dirname(os.path.abspath(__file__))

devnull = open(os.devnull, 'w')

if os.path.isdir(directory + '/envs'):
    shutil.rmtree(directory + '/envs')

os.mkdir(directory + '/envs')

pythons = [('Python 2.6', 'python2.6', '2'), ('Python 2.7', 'python2.7', '2'), ('Python 3.2', 'python3.2', '3'), ('Python 3.3', 'python3.3', '3'), ('Python 3.4', 'python3.4', '3'), ('Python 3.5', 'python3.5', '3'), ('PyPy', 'pypy', '2'), ('PyPy3', 'pypy3', '3')]

nonexistentmajorversions = []

for major in ['2', '3']:
    if subprocess.call(['which', 'python' + major], stdout=devnull, stderr=devnull) == 0:
        if subprocess.call(['python' + major, '-m', 'virtualenv', '--version'], stdout=devnull, stderr=devnull) != 0:
            print('Found python' + major + ' but could\'nt find virtualenv')
            print('Try `python' + major + ' -m pip install virtualenv`')
            nonexistentmajorversions.push(major)
    else:
        print('Couldn\'t find python' + major)

if nonexistentmajorversions:
    print('Environments with major version' + ('s' if len(nonexistentmajorversions) > 1 else '') + ' ' + ', '.join(nonexistentmajorversions) + ' will not be made')

for (name, executable, major) in pythons:
    if subprocess.call(['which', executable], stdout=devnull, stderr=devnull) != 0:
        print('Couldn\'t find ' + name + ', not making env')
    else:
        print('Making ' + name + ' env... ', end='')
        path = subprocess.check_output(['which', executable])[:-1]
        print('done' if subprocess.call(['python' + major, '-m', 'virtualenv', '-p', path, directory + '/envs/' + executable], stdout=devnull, stderr=devnull) == 0 else 'failed!')
