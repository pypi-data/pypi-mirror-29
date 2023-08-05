from setuptools import setup

setup(name='cwpythonwrapper',
      version='0.1.2',
      description='Python wrapper for Code Wars',
      author='Michiel Dockx',
      author_email='michieldx@gmail.com',
      url='https://bitbucket.org/Arvraepe-jstack/codewars',
      packages=['cwpythonwrapper', 'cwpythonwrapper/models'],
      install_requires=[
          'socketIO_client_nexus==0.7.6',
      ])
