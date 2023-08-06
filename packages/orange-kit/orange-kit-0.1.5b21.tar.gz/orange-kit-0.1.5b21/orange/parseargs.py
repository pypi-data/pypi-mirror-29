# 项目：标准库函数
# 模块：参数处理模块
# 作者：黄涛
# License:GPL
# Email:huangtao.sh@icloud.com
# 创建：2016-03-16 15:27

'''
参数处理模块。
'''
from argparse import ArgumentParser
import sys
from .htutil import *

class Argument():
    def __init__(self,*args,**kwargs):
        self.args=args
        self.kwargs=kwargs
        
    def add(self,parser):
        parser.parser.add_argument(*self.args,**self.kwargs)

Arg=Argument

class Parser():
    def __init__(self,*items,proc=None,allow_empty=False,**kwargs):
        deprecation("Parser","arg 和 command")
        self.items=items
        self.proc=proc
        self.kwargs=kwargs
        self.allow_empty=allow_empty
        self._subparsers=None

    def __call__(self,argv=None):
        self.parser=ArgumentParser(**self.kwargs)
        for item in self.items:
            item.add(self)
        argv=argv or sys.argv[1:]
        if self.allow_empty or argv:
            ns=self.parser.parse_args(argv)
            if self.proc:
                if isinstance(self.proc,str):
                    self.proc=eval(self.proc)
                args=dict(ns._get_kwargs())
                if self._subparsers:
                    subcommand=args.pop('subcommand',None)
                    if subcommand and hasattr(self.proc,subcommand):
                        self.proc=getattr(self.proc,subcommand)
                self.proc(**args)
        else:
            self.parser.print_usage()

    @property
    def subparsers(self):
        if not self._subparsers:
            self._subparsers=self.parser.add_subparsers(
                dest="subcommand",help="sub commands")
        return self._subparsers

class SubParser(Parser):
    def __init__(self,name,*items,help=None,**kwargs):
        self.name=name
        self.help=help
        super().__init__(*items,**kwargs)
        
    def add(self,parser):
        self.parser=parser.subparsers.add_parser(
            self.name,help=self.help,**self.kwargs)
        for item in self.items:
            item.add(self)
            
