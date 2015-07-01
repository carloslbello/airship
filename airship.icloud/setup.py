from setuptools import setup

setup(
    name='airship-icloud',
    version='1.4.0',

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
        'Programming Language :: Python :: 3.4'
    ],

    keywords='cloud games',

    packages=['airship'],

    install_requires=['airship']
)
