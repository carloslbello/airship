import os
import platform
import shutil


def cleanbin():
    path = os.path.dirname(os.path.abspath(__file__))
    system = platform.system()
    bits = platform.architecture()[0][:2]
    isosx = False
    binfolders = ['bin_win32', 'bin_win64', 'bin_osx', 'bin_lnx32',
                  'bin_lnx64']

    if system == 'Windows':
        binfolders.remove('bin_win' + bits)
    elif system == 'Darwin':
        binfolders.remove('bin_osx')
        isosx = True
    else:
        binfolders.remove('bin_lnx' + bits)

    for folder in binfolders:
        if os.path.isdir(os.path.join(path, folder)):
            shutil.rmtree(os.path.join(path, folder))

    if isosx and os.path.isdir(os.path.join(path, 'bin_osx')):
        import subprocess
        arch = os.uname()[4]
        for item in os.listdir(os.path.join(path, 'bin_osx')):
            if not item.startswith('.'):
                item = os.path.join(path, 'bin_osx', item)
                if not (subprocess.check_output(['lipo', '-info', item])
                        .startswith('Non-fat')):
                    beforedot = item[:item.rfind('.')]
                    afterdot = item[item.rfind('.'):]
                    lipoed = beforedot + '-lipo' + afterdot
                    subprocess.call(['lipo', item, '-output', lipoed, '-thin',
                                     arch])
                    os.rename(lipoed, item)
