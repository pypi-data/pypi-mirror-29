import os
from setuptools import setup, find_packages

# allow setup.py to be run from any path
HERE = os.path.realpath(os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(name='django_openehr',
      version='0.0.4',
      description='openEHR archetypes rendered as Django models',
      url='https://github.com/openhealthcare/django_openehr',
      author='Open Health Care UK',
      license='MIT',
      packages=find_packages(),
      zip_safe=False)
