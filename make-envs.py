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

pythons = [('python2.6', '2'), ('python2.7', '2'), ('python3.2', '3'), ('python3.3', '3'), ('python3.4', '3'), ('python3.5', '3'), ('pypy', '2'), ('pypy3', '3')]

nonexistentmajorversions = []

for major in ['2', '3']:
    if subprocess.call(['which', 'python' + major], stdout=devnull, stderr=devnull) == 0:
        if subprocess.call(['python' + major, '-m', 'virtualenv', '--version'], stdout=devnull, stderr=devnull) != 0:
            print('Found python' + major + ' but could\'nt find virtualenv')
            print('Try `python' + major + ' -m pip install virtualenv`')
            nonexistentmajorversions.append(major)
    else:
        print('Couldn\'t find python' + major)

if nonexistentmajorversions:
    print('Environments with major version' + ('s' if len(nonexistentmajorversions) > 1 else '') + ' ' + ', '.join(nonexistentmajorversions) + ' will not be made')

def get_python_ver(python):
    if executable.startswith('python'):
        name = 'Python'
    if executable.startswith('pypy'):
        name = 'PyPy'

    vflag = subprocess.Popen([executable, '-V'], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[1 if not (executable.startswith('python3.4') or executable.startswith('python3.5')) else 0][:-1]
    index = vflag.find(name) + len(name) + 1
    if executable.startswith('pypy3'):
        name = 'PyPy3'
    spaceindex = vflag.find(' ', index)
    if spaceindex == -1:
        ver = vflag[index:]
    else:
        ver = vflag[index:spaceindex]
    return (name, ver)

for (executable, major) in pythons:
    if not major in nonexistentmajorversions:
        if subprocess.call(['which', executable], stdout=devnull, stderr=devnull) != 0:
            print('Couldn\'t find ' + executable + ', not making env')
        else:
            name, ver = get_python_ver(executable)
            print('Making ' + name + ' ' * (7 - len(name)) + ver + ' ' * (7 - len(ver)) + 'env ... ', end='')
            path = subprocess.check_output(['which', executable])[:-1]
            print('done' if subprocess.call(['python' + major, '-m', 'virtualenv', '-p', path, directory + '/envs/' + executable], stdout=devnull, stderr=devnull) == 0 else 'failed!')
