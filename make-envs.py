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

pythons = [('python2.6', '2'), ('python2.7', '2'), ('python3.2', '3'), ('python3.3', '3'), ('python3.4', '3'), ('python3.5', '3'), ('pypy', '2'), ('pypy3', '3'), ('jython', '2')]

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
    print('Environments with major version' + ('s ' if len(nonexistentmajorversions) > 1 else ' ') + ', '.join(nonexistentmajorversions) + ' will not be made')


def get_python_ver(python):
    if executable.startswith('python'):
        name = 'CPython'
    elif executable.startswith('pypy'):
        name = 'PyPy'
    else:
        name = executable[0].upper() + executable[1:]

    vflag = subprocess.Popen([executable, '-V'], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[1 if not (executable.startswith('python3.4') or executable.startswith('python3.5')) else 0][:-1]
    stdlib = subprocess.check_output([executable, '-c', 'import sys;sys.stdout.write(\'{0}.{1}.{2}\'.format(*sys.version_info))'])
    index = vflag.find(name) + len(name) + 1
    if executable.startswith('pypy3'):
        name = 'PyPy3'
    spaceindex = vflag.find(' ', index)
    if spaceindex == -1:
        ver = vflag[index:]
    else:
        ver = vflag[index:spaceindex]
    return (name, ver, stdlib)

longestname = 0
longestver = 0
longeststdlib = 0

pythonsinstalled = []

for (executable, major) in pythons:
    if major not in nonexistentmajorversions:
        if subprocess.call(['which', executable], stdout=devnull, stderr=devnull) != 0:
            print('Couldn\'t find ' + executable + ', not making env')
        else:
            name, ver, stdlib = get_python_ver(executable)
            longestname = max(longestname, len(name))
            longestver = max(longestver, len(ver))
            longeststdlib = max(longeststdlib, len(stdlib) if stdlib != ver else 0)
            pythonsinstalled.append((executable, major, name, ver, stdlib))

python32envs = []

for (executable, major, name, ver, stdlib) in pythonsinstalled:
    print('Making ' + name + ' ' * (longestname + 1 - len(name)) + ver + ((' ' * (longestver + 1 - len(ver)) + '(stdlib ' + stdlib + ')' + ' ' * (longeststdlib + 1 - len(stdlib))) if stdlib != ver else (' ' * (longestver - len(ver) + longeststdlib + (11 if longeststdlib != 0 else 1)))) + 'env ... ', end='')
    path = subprocess.check_output(['which', executable]).rstrip()
    is32 = stdlib.startswith('3.2')
    if subprocess.call(['python' + major, '-m', 'virtualenv', '-p', path, directory + '/envs/' + executable] + (['--no-setuptools', '--no-pip', '--no-wheel'] if is32 else []), stdout=devnull, stderr=devnull) == 0:
        print('done')
        if is32:
            python32envs.append((executable, major, name, ver, stdlib))
    else:
        print('failed!')
        shutil.rmtree(directory + '/envs/' + executable)

if python32envs:
    longest32name = 0
    longest32ver = 0
    longest32stdlib = 0

    for (executable, major, name, ver, stdlib) in python32envs:
        longest32name = max(longest32name, len(name))
        longest32ver = max(longest32ver, len(ver))
        longest32stdlib = max(longest32stdlib, len(stdlib) if stdlib != ver else 0)

    for (executable, major, name, ver, stdlib) in python32envs:
        print('Packages for ' + name + ' ' * (longest32name + 1 - len(name)) + ver + ((' ' * (longest32ver + 1 - len(ver)) + '(stdlib ' + stdlib + ')' + ' ' * (longest32stdlib + 1 - len(stdlib))) if stdlib != ver else (' ' * (longest32ver - len(ver) + longest32stdlib + (11 if longest32stdlib != 0 else 1)))) + 'env ... ', end='')
        execfile(directory + '/envs/' + executable + '/bin/activate_this.py', dict(__file__=directory + '/envs/' + executable + '/bin/activate_this.py'))
        if subprocess.call(['python', directory + '/get-pip-32.py', 'setuptools<18.5', 'pip<8', 'wheel'], stdout=devnull, stderr=devnull) == 0:
            print('done')
        else:
            print('failed!')
            shutil.rmtree(directory + '/envs/' + executable)
