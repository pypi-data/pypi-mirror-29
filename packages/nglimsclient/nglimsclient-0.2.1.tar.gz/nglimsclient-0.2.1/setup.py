import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'VERSION')) as f:
    __version__ = f.read().strip()

with open(os.path.join(here, 'requirements.txt')) as f:
    required = f.read().splitlines()

with open(os.path.join(here, 'README.rst')) as f:
    long_description = f.read()

extra_files = [os.path.join(here, 'requirements.txt'),
               os.path.join(here, 'README.rst'),
               os.path.join(here, 'VERSION'),
               ]

AuthorInfo = (
    ("Gianmauro Cuccuru", "gmauro@crs4.it"),
    ("Luca Lianas", "lianas@crs4.it"),
    ("Luca Pireddu", "pireddu@crs4.it"),
    ("Rossano Atzeni", "ratzeni@crs4.it"),
)

setup(name="nglimsclient",
      version=__version__,
      description="nglims client package for bioblend",
      long_description=long_description,
      author=",".join(a[0] for a in AuthorInfo),
      author_email=",".join("<%s>" % a[1] for a in AuthorInfo),
      zip_safe=True,
      url='https://bitbucket.org/crs4/nglimsclient',
      packages=find_packages(exclude=('tests',)),
      keywords='utilities',
      install_requires=required,
      package_data={'': extra_files},
      license='MIT',
      platforms="Posix; MacOS X; Windows",
      classifiers=["Development Status :: 4 - Beta",
                   "Intended Audience :: Developers",
                   "License :: OSI Approved :: MIT License",
                   "Operating System :: OS Independent",
                   "Topic :: Internet",
                   "Programming Language :: Python :: 2.7",
                   ],
      )
