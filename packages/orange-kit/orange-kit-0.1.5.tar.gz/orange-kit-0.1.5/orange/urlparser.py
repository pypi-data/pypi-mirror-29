# 项目：标准库函数
# 模块：网而数据分析
# 作者：黄涛
# License:GPL
# Email:huangtao.sh@icloud.com
# 创建：2016-11-19 16:56


from urllib import parse,request
from bs4 import BeautifulSoup as BeautifulSoup
from orange.path import *
from threading import Thread

def url_open(url,data=None,features='lxml',proc=None,**kw):
    '''打开网页，并分析其内容
    url: 指定的网页
    data: 查询参数
    proc: 分析程序
    kw:   其他传递给BeautifulSoup的参数
    '''
    if data:
        url='%s?%s'%(url,parse.urlencode(data))
    with request.urlopen(url) as fn:
        data=fn.read()
        markup=decode(data)
    soup=BeautifulSoup(markup,features,**kw)
    if callable(proc):
        proc(soup)
    return soup

def turl_open(*args,**Kw):
    '''以线程的方式打开网页，函数说明同 url_open'''
    Thread(target=url_open,args=args,kwargs=kw).start()
    
