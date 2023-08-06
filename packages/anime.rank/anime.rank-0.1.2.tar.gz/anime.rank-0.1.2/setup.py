# -*- encoding: UTF-8 -*-
from setuptools import setup, find_packages

VERSION = '0.1.2'

setup(name='anime.rank',
      version=VERSION,
      description='anime rank',
      keywords='python anime rank',
      author='csi0n',
      author_email='chqssqll@gmail.com',
      url='https://github.com/csi0n/AnimeRank',
      license='MIT',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=True,
      install_requires=[
          'requests_html', 'click'
      ],
      entry_points={
          'console_scripts': [
              'anime.rank=AnimeRank.main:main'
          ]
      }
      )
