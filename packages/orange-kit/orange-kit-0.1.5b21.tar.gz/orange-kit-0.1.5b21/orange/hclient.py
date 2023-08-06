# 项目：标准库函数
# 模块：网络爬虫
# 作者：黄涛
# License:GPL
# Email:huangtao.sh@icloud.com
# 创建：2016-12-26 17:08
# 修订：2017-01-14

from aiohttp import *
from orange.coroutine import *
from orange import *
from bs4 import BeautifulSoup as BS4

__all__='Crawler','wait','BS4'

class Crawler(ClientSession):
    root=''   # 网址的根目录
    def __init__(self,root=None,*args,**kw):
        if root:
            if root.endswith('/'):
                root=root[:-1]
            self.root=root    # 设置根目录
        super().__init__(*args,**kw)

    def _request(self,method,url,*args,**kw):
        # 处理网址，支持网址中只输入后续路径
        if ':' not in url:
            if url.startswith('/'):
                url=url[1:]
            url='/'.join([self.root,url])
        return super()._request(method,url,*args,**kw)
    
    async def get_text(self,url,*args,method='GET',**kw):
        # 以获取指定网页的文本
        async with self.request(method,url,*args,**kw)as resp:
            return await resp.text()

    async def get_soup(self,url,*args,**kw):
        # 获取指定网页的BeautifulSoup实例
        text=await self.get_text(url,*args,**kw)
        return BS4(text,'lxml')

    async def download(self,url,params=None,path='.',*args,**kw):
        # 下载文件，其中path可以是下载文件的文件名，也可以是下载目录
        async with self.get(url,params=params,*args,**kw)as resp:
            path=Path(path)
            if path.is_dir():
                from urllib.parse import unquote
                # 获取文件名字段
                filename=resp.headers['Content-Disposition'] 
                filename=filename.split(';')[-1]  # 获取最后一个参数
                tp,filename=filename.split('=')
                if tp.strip()=='filename*':
                    filename=(filename.split("'"))[-1]
                if filename.startswith('"'):
                    filename=filename[1:-1]
                filename=unquote(filename)
                path=path / Path(filename).name
            path.write(data=await resp.read()) # 写入文件
                    
    async def get_json(self,url,*args,encoding=None,method='GET',
                           **kw):
        # 获取指定网页的JSON数据
        async with self.request(method,url,*args,**kw)as resp:
            return await resp.json(encoding=encoding)

    async def run(self):
        # 爬虫的主运行程序
        raise Exception('This function doesn''t exist!')

    @classmethod
    def start(cls,target=None,args=None,kwargs=None,**kw):
        # target：待执行的命令，必须为协程，若无，则调用run
        # target的第一个参数应为 session
        # args：target的位置参数
        # kwargs: target的关键字参数
        # kw: cls的关键字参数
        args=args or []
        kwargs=kwargs or {}
        target=target or cls.run
        async def _main():
            async with cls(**kw)as sess:
                await target(sess,*args,**kwargs)
        start(_main())
 
