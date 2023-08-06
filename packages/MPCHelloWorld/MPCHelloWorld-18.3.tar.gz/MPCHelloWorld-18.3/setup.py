#!/usr/bin/env python
import sys
import os
from setuptools import setup
#from numpy.distutils.core import setup, Extension

#if "publish" in sys.argv[-1]:
#    os.system("python setup.py sdist")
#    os.system("twine upload dist/*")
#    os.system("rm -rf dist/*")
#    sys.exit()




# Load the __version__ variable without importing the package
#exec(open('HW/version.py').read())
exec(open('version.py').read())



setup(name='MPCHelloWorld',
      version=__version__,
      description="Simple, bare-bones package tofFacilitate MPC development",
      # long_description=long_description,
      author='Matt Payne',
      author_email='matthewjohnpayne@gmail.com',
      license='MIT',
      url='https://mpaynesedun209@bitbucket.org/mpcdev/mpchelloworld.git',
      packages=['MPCHelloWorld'],
      python_requires='>=3',
      #install_requires=["numpy"], ### Moved to requirements.txt 
      classifiers=[
              "Development Status :: 3 - Alpha",
              "License :: OSI Approved :: MIT License",
              "Operating System :: OS Independent",
              "Programming Language :: Python",
              "Intended Audience :: Science/Research",
              "Topic :: Scientific/Engineering :: Astronomy", ],
      )
