# -*- coding: utf-8 -*-import re
import os
import sys
try:
    from setuptools import setup, find_packages
except ImportError:
    sys.exit("error: install setuptools")

try:
    import subprocess
except ImportError:
    sys.exit("error: install subprocess. See installation instructions.")

def readme():
    with open('README.rst') as f:
        return f.read()
def is_tool(name,message):
    try:
        devnull = open(os.devnull)
        subprocess.Popen([name], stdout=devnull, stderr=devnull).communicate()
    except OSError as e:
        if e.errno == os.errno.ENOENT:
            sys.exit(message)
    return True

is_tool("bowtie2","Error: please install bowtie2. See installation instructions.")
is_tool("cutadapt","Error: please install cutadapt. See installation instructions.")
is_tool("bedtools","Error: please install bedtools. See installation instructions.")
is_tool("samtools","Error: please install samtools. See installation instructions.")

setup(name='UTRme',
      version='0.2.3.7',
      description='UTRme',
      long_description = readme(),
      author='Santiago Radio',
      author_email='sradio91@gmail.com',
      license='Laboratorio de Interacciones Moleculares',
      packages=find_packages(),
      python_requires='>=3',
      entry_points={'console_scripts': ['utrme = UTRme.utrme:main']},
      setup_requires = ['numpy'],
      install_requires=['xlsxwriter','scipy','python-levenshtein','fuzzywuzzy','regex','pyfaidx','pysam','gooey','pandas','BioPython','argparse','twine','matplotlib','seaborn'],
      keywords=['UTRme', 'splice-leader', 'polyA'],
      zip_safe=False
      )
