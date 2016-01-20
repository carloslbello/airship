from setuptools import setup

setup(
    name='airship-steamcloud',
    version='1.5.3',

    description='Steam Cloud plugin for Airship',

    url='https://github.com/aarzee/airship',

    author='Carlos Liam',
    author_email='carlos@aarzee.me',

    license='MIT',

    classifiers=[
        'Development Status :: 4 - Beta',

        'Intended Audience :: End Users/Desktop',
        'Topic :: Utilities',
        'Topic :: Internet',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5'
    ],

    keywords='cloud games',

    packages=['airship'],

    package_data={
        'airship': ['bin_win32/steam_api.dll', 'bin_win32/CSteamworks.dll', 'bin_win64/steam_api64.dll', 'bin_win64/CSteamworks.dll', 'bin_osx/libsteam_api.dylib', 'bin_osx/CSteamworks.dylib', 'bin_lnx32/libsteam_api.so', 'bin_lnx32/libCSteamworks.so', 'bin_lnx64/libsteam_api.so', 'bin_lnx64/libCSteamworks.so']
    },

    install_requires=['airship']
)
#@macosx=macosx_10_6_intel
