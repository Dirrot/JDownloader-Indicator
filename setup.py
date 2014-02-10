#!/usr/bin/env python2

from distutils.core import setup
from os.path import abspath
from os.path import join as path_join
from os import getcwd
from shutil import rmtree

pathname		=		getcwd()

packages        =       ['IndicatorJDownloader']

setup(name		    =		'IndicatorJDownloader JDownloader (Remote API)',
      version		=		'0.1',
      description	=		'Python indicator for the JDownloader remote api.',
      author		=		'Dirrot',
      author_email  =       'dirrot@web.de',
      url		    =		'https://github.com/Dirrot/python-indicator-jdownloader-remote',
      packages		=		packages,
      package_dir	=		{
                               'JDownloader.py' : abspath(path_join(pathname, 'IndicatorJDownloader/')), 
                               'JDRemote.py' : abspath(path_join(pathname, 'IndicatorJDownloader/'))
                            },
      data_files	=		[
                              ('share/IndicatorJDownloader', ['README.md', 'LICENSE','img/donation-qr-code.png']),
                              ('share/IndicatorJDownloader/icons', ['IndicatorJDownloader/icons/jd.png', 'IndicatorJDownloader/icons/jd_ubuntu.png']),
                              ('/usr/bin', ['scripts/indicator-jdownloader'])
                            ],
      

	)


try:
	rmtree(abspath(path_join(pathname, 'build/')))
except:
	pass
