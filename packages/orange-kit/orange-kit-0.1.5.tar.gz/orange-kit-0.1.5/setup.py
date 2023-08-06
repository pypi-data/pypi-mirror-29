#!/usr/bin/env python3
from orange import setup

console_scripts = ['conv=orange.path:convert',
                   #'pytest=orange.pytools:pytest',
                   'pysdist=orange.pytools:pysdist',
                   'pyupload=orange.pytools:pyupload',
                   'canshu=orange.ggcs:canshu',
                   #'mongodb=orange.mongodb:main',
                   'pyver=orange.pyver:VersionMgr.main',
                   'plist=orange.plist:main',
                   'pyinit=orange.init:main',
                   'gclone=orange.gclone:proc',
                   'mongodeploy=orange.mongodb:main',
                   'fkgfw=orange.fkgfw:main',
                   'sysinit=orange.sysinit:main']
setup(
    name='orange-kit',
    platforms='any',
    description='orange',
    long_description='orange',
    url='https://github.com/huangtao-sh/orange.git',
    cscripts=console_scripts,
    # entry_points={'console_scripts':console_scripts},
        license='GPL',
)
