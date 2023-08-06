#!/usr/bin/env python3
# 项目：标准库
# 模块：版本管理程序
# 作者：黄涛
# License:GPL
# Email:huangtao.sh@icloud.com
# 创建：2015-05-20 15:32
# 修订：2016-9-6 将其迁移至orange 库，并移除对stdlib 的依赖
# 修订：2017-2-10 pyver 增加 -y 功能，与远程服务器同步

import os
import sys
from orange import *
from orange.version import Ver
from orange.parseargs import *
from .pytools import pyupload,pysdist

class VersionMgr:
    branch=None   # 当前git分支
    up_to_date=True  # 与版本库是否同步
    untracted_files=[]  # 未跟踪文件 
    not_staged=[]       # 已更新文件
    to_be_commited=[]   # 待提交文件
    is_clean=False      # 工作区是否干净
    ver=None            # 当前程序版本
    repository=True     # 是否纳入git版本管理
    file_type=None
    def proc_git(self):
        from re import compile
        patterns={
            compile(r'On branch (?P<branch>\w+)'):
            lambda branch:setattr(self,'branch',branch),
            compile(r"Your branch is up-to-date with '.*?'."):
            lambda :setattr(self,'up_to_date',True),
            compile(r"Changes not staged for commit:"):
            lambda :setattr(self,'file_type','not_staged'),
            compile(r"Untracked files:"):
            lambda :setattr(self,'file_type','untracted_files'),
            compile(r"Changes to be committed:"):
            lambda :setattr(self,'file_type','to_be_commited'),
            compile(r"\t(.*?:\s*)?(?P<file>.*)"):
            lambda file:getattr(self,self.file_type).append(file),
            compile(r"nothing to commit"):
            lambda :setattr(self,'is_clean',True)
            }
            
        s=read_shell('git status')  # 读取git状态
        if s ==[]:
            self.repository=False   
            return
        for line in s:
            for k,v in patterns.items():
                r=k.match(line)
                if r:
                    v(**r.groupdict())
                    break

    def __init__(self):
        if Path('.git').is_dir():
            self.ver=Ver.read_file()
            if self.ver:
                self.proc_git()

    def write_version_file(self,ver):
        self.ver.write_file()
        
    def show_version(self):     # 显示版本号与git状态
        if self.repository:
            print('\n当前分支： %s'%(self.branch))
            print('远程版本最否最新：%s'%(self.up_to_date))
            print('工作区是否干净：%s'%(self.is_clean))
            if self.ver:
                print('当前版本文件名：%s'%(self.ver.filename))
                print('当前程序版本：%s'%(self.ver))
        else:
            print('没有纳入GIT管理')
    
    def commit_(self):        # 提交变更
        if self.branch=='master':
            raise Exception('错误：当前git分支必须不能为master')
        if self.is_clean:
            raise Exception('错误：当前工作区无待提交的更改')
        if not self.ver.prerelease: 
            raise Exception('错误：当前版本为最终版')
        if self.untracted_files:
            print('下面的文件没有被纳入git监控:')
            [print('\t%s'%(file_name)) for file_name in \
                   self.untracted_files]
            cmd=None
            while cmd not in ('a','A','y','Y','n','N'):
                cmd=input(
                    '请选择： Y-全部跟踪,N-全部不跟踪,A-放弃操作：')
                if cmd in ('a','A'):
                    print("放弃本次操作，程序退出")
                    return
                elif cmd in ('y','Y'):
                    self.not_staged.extend(self.untracted_files)
                    
        if self.not_staged:
            print('以下文件将被提交到git')
            [print('\t%s'%(fil)) for fil in self.not_staged]
            [exec_shell('git add "%s"'%(fil)) for fil in\
                        self.not_staged]
            self.to_be_commited.extend(self.not_staged)
            
        if self.to_be_commited:
            if self.ver:
                ver=str(self.ver)
                self.ver.upgrade()
                print('版本号由%s升级到%s'%(ver,self.ver))
                self.ver.write_file()
                exec_shell('git commit -a -m "%s"'%(self.commit))
                exec_shell('git push --all')
                    
    def upgrade_ver(self):
        from distutils.version import StrictVersion as Version
        ver=self.ver
        if self.branch=='master':
            raise Exception('错误：当前git分支必须不能为master')

        if self.upgrade not in ('major','minor','micro','dev','p','patch',
                                'm','n','o','d'):
            raise Exception('错误：参数输入错误')

        if not self.is_clean and self.upgrade in ('d','dev',):
                raise Exception('错误：当前工作区有待提交的更改')

        if self.upgrade in ('d','dev')and ver.prerelease is None:
            raise Exception('错误：已经是最终版本')

        if self.upgrade not in ('d','dev')and ver.prerelease:
            raise Exception('错误：当前版本非最终版')

        if self.ver:
            self.ver.upgrade(self.upgrade)
            print('版本号由%s升级到%s'%(ver,self.ver))
            self.ver.write_file()
            ver=self.ver
            if ver.prerelease is None:
                cmds=['git commit -a -m "升级到最终版"',
                      'git checkout master',
                      'git merge %s'%(self.branch),
                      'git tag ver%s'%(self.ver),
                      'git checkout %s'%(self.branch),
                      'git push --all',
                      'git push --tags',
                      'pysdist',
                      'pysetup']
                for cmd in cmds:
                    exec_shell(cmd)

    def sync(self):
        s=read_shell('git status')
        if 'working directory clean' not in s[-1]:
            print(*s,sep='\n')
        elif "Your branch is ahead of" in s[1]:
            os.system('git push --all')
        os.system('git pull --all')
        
    @classmethod
    @arg('-u','--upgrade',nargs='?',action='store',
                metavar='segment',help=('升级版本号，可以为major,'
                'minor,micro,dev'))
    @arg('-c','--commit',nargs='?',metavar='message',help='提交变更')
    @arg('-s','--show',action='store_true',help='查看当前版本状态')
    @arg('-y','--sync',action='store_true',help='同步程序')
    @arg('-d','--sdist',action='store_true',help='源代码打包')
    @arg('-U','--upload',action='store_true',help='打包上传')
    def main(cls,show=None,upgrade=None,commit=None,sync=False,
                 sdist=False,upload=False):
        obj=cls()
        if obj:
            if show:
                obj.show_version()
            if commit:
                obj.commit=commit
                obj.commit_()
            if upgrade:
                obj.upgrade=upgrade
                obj.upgrade_ver()
            if sync:
                obj.sync()
            if upload:
                pyupload()
            if sdist:
                pysdist()
                
Pattern=R/r'\d+(\.\d+)*([ab]\d+)?'

def find_ver(path):
    v=Pattern.search(str(path))
    if v:
        return Ver(v.group())

def get_cur_ver(paths):
    if paths:
        return list(sorted(paths,key=lambda x:find_ver(x)))[-1]
        
