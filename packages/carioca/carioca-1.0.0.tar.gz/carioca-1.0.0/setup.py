import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

version={}
exec(open('carioca/version.py').read(), version)
setup(
    name='carioca',
    version=version['__version__'],
    packages=['carioca'],
    install_requires=['pyserial', 'xmodem'],
    include_package_data=True,
    entry_points= {
        'console_scripts': [
            'carioca = carioca.carioca:main'
        ]
    },
    license='MIT License',  # example license
    description='Interface to Atmel SAM-BA Monitor.',
    long_description=README,
    url='https://bitbucket.org/egauge/carioca/',
    author='David Mosberger-Tang',
    author_email='davidm@egauge.net',
    classifiers=[
        'Development Status :: 3 - Alpha',
    ],
)
