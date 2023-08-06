# 项目：标准库函数
# 模块：程序版本模块
# 作者：黄涛
# License:GPL
# Email:huangtao.sh@icloud.com
# 创建：2016-03-11 12:59
# 修订：2016-09-10 增加Ver 类来管理版本
from orange.path import Path
from distutils.version import StrictVersion
from orange.debug import *

SEGMENT={'major':0,'m':0,
        'minor':1,'n':1,
        'micro':2,'o':2,
        'patch':2,'p':2,
        'dev':3,'d':3,
        '#':4,}

first=lambda x:x and x[0]
last=lambda x:x and x[-1]

class Ver(StrictVersion):
    '''自定义版本管理程序
    增加upgrade功能
    '''
    def upgrade(self,segment=4):
        '''升级版本号
        其中参数 segment可以为：
        major:升级主版本号
        minor:升级小版本号
        patch:升级补丁版本号
        dev:升级开发版本号
        #:升级开发版本序号
        '''
        if isinstance(segment,str):
            segment=SEGMENT.get(segment.lower(),4)
        if segment<3:
            ensure(not self.prerelease,
                   '开发版本号不允许直接升级正式版本号！')
        else:
            ensure(self.prerelease,'正式版本号不允许升级开发版本号')
        if segment==4:
            self.prerelease=self.prerelease[0],self.prerelease[1]+1
        elif segment==3:
            if self.prerelease[0]=='a':
                self.prerelease='b',1
            else:
                self.prerelease=None
        else:
            self.prerelease='a',1
            nv=list(self.version)
            nv[segment]+=1
            for x in range(segment+1,3):
                nv[x]=0
            self.version=tuple(nv)
        return self

    @classmethod
    def read_file(cls,filename=None):
        '''从版本文件中读取版本号'''
        if not filename:
            filename=first(list(Path('.').glob('*/__version__.py')))
        if filename:
            for line in Path(filename).lines:
                if line.startswith('version'):
                    ver=cls(line.split('"')[1])
                    ver.filename=filename
                    return ver

    def write_file(self,filename=None):
        '''将版号写入版本文件中'''
        filename=filename or self.filename
        Path(filename).text='version="%s"\n'%(self)
                    
def get_ver():
    '''该函数将会被废弃'''
    ver_file=first(list(Path(".").glob("*/__version__.py")))
    if ver_file:
        for line in ver_file.lines:
            if line.startswith('version'):
                return line.split('"')[1]

def upgrade_ver(ver,segment='#'):
    '''该函数将被废弃'''
    if not isinstance(ver,Ver):
        ver=Ver(ver)
    if isinstance(segment,str):
        segment={'major':0,
                 'm':0,
                 'minor':1,
                 'n':1,
                 'micro':2,
                 'o':2,
                 'dev':3,
                 'd':3,
                 '#':4,}.get(segment.lower(),4)
    if(ver.prerelease and segment<3)or(not ver.prerelease and segment>=3):
        raise Exception('版本升级失败')
    if segment==4:
        ver.prerelease=ver.prerelease[0],ver.prerelease[1]+1
    elif segment==3:
        if ver.prerelease[0]=='a':
            ver.prerelease='b',1
        else:
            ver.prerelease=None
    else:
        ver.prerelease='a',1
        nv=[0,0,0]
        nv[:segment+1]=ver.version[:segment+1]
        nv[segment]+=1
        ver.version=tuple(nv)
    return ver
        
            
