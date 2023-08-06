try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from os import path

README = path.abspath(path.join(path.dirname(__file__), 'README.rst'))

setup(
      name='flask_redis_log',
      version='0.0.1',
      description='Redis pub/sub logging handler for python',
      long_description=open(README).read(),
      author='Luis Diego Cordero',
      author_email='ldiego@gmail.com',
      url='https://gitlab.wearegap.com/lcordero/flask-redis-logs.git',
      packages=['redislogs'],
      license='MIT',
      install_requires=['redis']
)