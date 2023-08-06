import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'APPNAME')) as f:
    __appname__ = f.read().strip()

with open(os.path.join(here, 'VERSION')) as f:
    __version__ = f.read().strip()

with open(os.path.join(here, 'requirements.txt')) as f:
    required = f.read().splitlines()

with open(os.path.join(here, 'README.rst')) as f:
    long_description = f.read()

extra_files = [os.path.join(here, 'APPNAME'),
               os.path.join(here, 'requirements.txt'),
               os.path.join(here, 'README.rst'),
               os.path.join(here, 'VERSION'),
               ]

setup(
    name=__appname__,
    version=__version__,
    description='useful functions and classes',
    long_description=long_description,
    author='Gianmauro Cuccuru',
    author_email='gmauro@gmail.com',
    zip_safe=True,
    url='http://github.com/gmauro/comoda',
    license='MIT',
    packages=find_packages(exclude=('tests',)),
    keywords='utilities',
    install_requires=required,
    package_data={'': extra_files},
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ],
)
