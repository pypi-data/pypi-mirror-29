#from distutils.core import setup
from setuptools import setup, find_packages

setup(
  name = 'orbis-client-test',
  packages = find_packages(), # this must be the same as the name above
  version = '0.2.3',
  description = 'A random test lib',
  author = 'Chanwoo Lee',
  author_email = 'cjswosa2@gmail.com',
  url = 'https://github.com/peterldowns/mypackage', # use the URL to the github repo
  download_url = 'https://github.com/leechanwoo/orbistest/blob/master/tfclient_package/package.tar', # I'll explain this in a second
  keywords = ['testing', 'logging', 'example'], # arbitrary keywords
  classifiers = [],
  install_requires=[
      'tensorflow>=1.4',
      'scipy>=0.9',
      'numpy>=1.0'
      ],
)
