# 项目：标准库函数
# 模块：markdown扩展
# 作者：黄涛
# License:GPL
# Email:huangtao.sh@icloud.com
# 创建：2016-03-24 19:57

import mistune
import re
class Extension:
    gramar=r''
    name=''
 
    def output(self,*args,**kwargs):
        return ""
    
class InlineExtension(Extension):
    @classmethod
    def update(cls,markdown):
        setattr(markdown.inline.rules,
                cls.name,re.compile(cls.grammar))
        setattr(markdown.inline.__class__,
                'output_%s'%(cls.name),cls.output)
        markdown.inline.default_rules.append(cls.name)

class BlockExtension(Extension):
    def parse(self,*args,**kwargs):
        pass
    
    @classmethod
    def update(cls,markdown):
        setattr(markdown.block.rules,
            cls.name,re.compile(cls.grammar))
        setattr(markdown.block.__class__,
                'output_%s'%(cls.name),cls.output)
        markdown.block.default_rules.insert(0,cls.name)
        setattr(markdown.block.__class__,
                'parse_%s'%(cls.name),cls.parse)
                
class Markdown(mistune.Markdown):
    def __init__(self,extensions=None,**kw):
        super().__init__(**kw)
        if extensions:
            for extension in extensions:
                extension.update(self)
                
class Toc(BlockExtension):
    grammar=r'^\[toc\](\n+|$)'
    name='toc'
    def parse(self,m):
        self.tokens.append({'type':'toc'})

    def output(self):
        return ""

def get_links(text):
    parser=mistune.BlockLexer()
    parser(text)
    return parser.def_links

class BlockLexer(mistune.BlockLexer):
    def __call__(self,*args,**kw):
        result=super().__call__(*args,**kw)
        for k,v in self.def_links.items():
            v['link']='http://localhost/image/%s'%(v['link'])
        return result

s='''
This is a picture.

![sf]

[sf]: a/b.jpg "hello"
'''

m=Markdown(block=BlockLexer())
print(m(s))
