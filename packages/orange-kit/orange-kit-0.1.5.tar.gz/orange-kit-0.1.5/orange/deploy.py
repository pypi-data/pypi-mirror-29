# 项目：标准库函数
# 模块：安装模块
# 作者：黄涛
# License:GPL
# Email:huangtao.sh@icloud.com
# 创建：2016-03-12 18:05

import distutils.core
import os
import setuptools
import pip
from orange import Path,Ver

def get_path(pkg,user=True):
    ''' 返回指定包的参数配置目录和数据目录'''
    if os.name=='posix':
        if user:
            root=Path('~')
            return root,root/ ('.%s'%(pkg))
        else:
            root=Path('/usr/local')
            return root/'etc',root/'var'/pkg
    else:
        if user:
            root=Path('~/AppData')
            return root /'Roaming' ,root / 'Local' / pkg
        else:
            root=Path('%programdata%') / pkg
            return root,root
            
def run_pip(*args):
    pip.main(list(args))
    
def run_setup(*args):
    distutils.core.run_setup('setup.py',args)

DEFAULT={'author':'huangtao',
         'author_email':'huangtao.sh@icloud.com',
         'platforms':'any',
         'license':'GPL',}

def _get_requires():
    result=[]
    for fn in Path('.').glob('*/requires.txt'):
        for row in fn.lines:
            i=row.find('#')
            if i>-1:
                row=row[:i]
            row=row.strip()
            if row:
                result.append(row)
    return result
            
def setup(version=None,packages=None,after_install=None,
          scripts=None,install_requires=None,
          cscripts=None,gscripts=None,
          **kwargs):
    if cscripts or gscripts:
        entry_points=kwargs.get('entry_points',{})
        if cscripts:
            entry_points['console_scripts']=cscripts
        if gscripts:
            entry_points['gui_scripts']=gscripts
        kwargs['entry_points']=entry_points
    for k,v in DEFAULT.items():
        kwargs.setdefault(k,v)
    if not packages:
        # 自动搜索包
        packages=setuptools.find_packages(exclude=('testing',
                                                   'scripts'))
    if not version:
        # 自动获取版本
        version=str(Ver.read_file())
    if not install_requires: # 从repuires.txt 中获取依赖包
        install_requires=_get_requires()
    if not scripts:
        scripts=[str(path) for path in Path('.').glob('scripts/*')]
    # 安装程序 
    dist=distutils.core.setup(scripts=scripts,packages=packages,
            install_requires=install_requires,
            version=version,**kwargs)
    # 处理脚本

    if 'install' in dist.have_run and os.name=='posix' \
      and scripts:
        from sysconfig import get_path
        prefix=Path(get_path('scripts'))
        for script in scripts:
            script_name=prefix/(Path(script).name)
            if script_name.lsuffix in ['.py','.pyw']\
              and script_name.exists():
                script_name.replace(script_name.with_suffix(''))
    if 'install' in dist.have_run and after_install:
        after_install(dist)
