from setuptools import setup

setup(
    name='airship-icloud',
    version='1.5.1',

    description='iCloud plugin for Airship',

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

    install_requires=['airship']
)
# !@any=macosx_10_7_universal
# ^ pip 7.1.2, the last version to support Python 3.2, does not generate tags
#   matching py2.py3-none-macosx_10_7_universal, so we can't use this
#   https://github.com/pypa/pip/issues/3202
