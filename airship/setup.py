from setuptools import setup

setup(
    name='airship',
    version='1.4.6',

    description='A tool to synchronize game saves between clouds',
    long_description='Airship allows users to synchronize saved games between cloud platforms. Requires subpackages for each cloud service; for example, install airship-steamcloud and airship-icloud to sync between these two services.',

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

    extras_require={
        ':python_version=="2.6"': ['argparse']
    },

    entry_points={
        'console_scripts': [
            'airship=airship:main'
        ]
    }
)
