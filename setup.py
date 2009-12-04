# -*- coding: UTF-8 -*-
#!/usr/bin/env python

from __future__ import with_statement

import sys
import os.path
import string

from distutils.command.build_py import build_py as _build_py
from setuptools import setup

class build_py(_build_py):
    """build_py command

    This specific build_py command will modify module 'build_config' so that it
    contains information on installation prefixes afterwards.
    """
    def build_module (self, module, module_file, package):
        if isinstance(package, str):
            package = package.split('.')
        elif not isinstance(package, (list, tuple)):
            raise TypeError(
                "'package' must be a string (dot-separated), list, or tuple")

        if ( module == 'build_info' and len(package) == 1 and package[0] == 'mwdb'):
            iobj = self.distribution.command_obj['install']

            with open(module_file, 'w') as module_fp:
                module_fp.write('# -*- coding: UTF-8 -*-\n\n')
                module_fp.write("DATA_DIR = '%s'\n"%(
                    os.path.join(iobj.install_data, 'share')))
                module_fp.write("LIB_DIR = '%s'\n"%(iobj.install_lib))
                module_fp.write("SCRIPT_DIR = '%s'\n"%(iobj.install_scripts))

        _build_py.build_module(self, module, module_file, package)

extra = {}
if sys.version_info >= (3,):
    extra['use_2to3'] = True

setup(name='mwdb',
      version='0.1a',
      description='MediaWiki database API',
      author='Wolodja Wentland',
      author_email='wentland@cl.uni-heidelberg.de',
      url='http://github.com/babilen/mwdb',
      license='GPLv3',
      packages=['mwdb', 'mwdb.orm', 'mwdb.orm.tables', 'mwdb.mediawiki',
               ],
      package_dir = { '':'lib' },
      cmdclass={'build_py': build_py },
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: GNU General Public License (GPL)'
          'Programming Language :: Python',
          'Topic :: Database',
          'Topic :: Scientific/Engineering',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Topic :: Text Processing',
      ],
      **extra
     )
