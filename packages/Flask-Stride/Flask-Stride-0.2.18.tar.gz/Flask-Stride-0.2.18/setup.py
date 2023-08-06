from setuptools import setup

setup(
  name = 'Flask-Stride',
  packages = ['flask_stride'],
  version = '0.2.18',
  description = 'Flask adapter client for pystride',
  author = 'Dave Chevell',
  author_email = 'dchevell@atlassian.com',
  url = 'https://bitbucket.org/dchevell/flask-stride',
  keywords = ['atlassian', 'stride', 'flask'],
  classifiers = [],
  license = 'MIT',
  install_requires = ['pystride', 'Flask']
)
