from distutils.core import setup
from setuptools import find_packages

setup(name='pyriver',
      packages=find_packages(exclude=['dist']),
      version='0.0.1.9',
      description='River client.',
      url='http://github.com/ptbrodie/pyriver',
      author='Patrick Brodie',
      author_email='ptbrodie@gmail.com',
      install_requires=[
        'beautifulsoup4==4.6.0',
        'Flask==0.12.2',
        'Flask-SQLAlchemy==2.3.2',
        'gunicorn==19.7.1',
        'redis==2.10.6',
        'requests==2.18.4',
        'schedule==0.5.0',
        'sqlalchemy==1.2.1',
      ],
      entry_points={"console_scripts": ["river-server=pyriver.server:run_server"]},
      scripts=['./river'])
