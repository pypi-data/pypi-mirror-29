# 项目：标准库函数
# 模块：运行库
# 作者：黄涛
# License:GPL
# Email:huangtao.sh@icloud.com
# 创建：2016-04-13 20:46

import os

class classproperty:
    '''类属性，用法：
    class A:
        @classproperty
        def name(cls):
              return cls.__name__

    A.name
    A().name
    '''

    def __init__(self, getter):
        self.getter = getter

    def __get__(self, instance, kclass):
        return self.getter(kclass)


class cachedproperty:
    '''类属性，用法：
    class A:
        @classproperty
        def name(cls):
              return cls.__name__

    A.name
    A().name
    '''

    def __init__(self, getter):
        self.getter = getter
        self.cache = {}

    def __get__(self, instance, kclass):
        if kclass not in self.cache:
            self.cache[kclass] = self.getter(kclass)
        return self.cache[kclass]


def read_shell(cmd):
    '''
    执行系统命令，并将执行命令的结果通过管道读取。
    '''
    with os.popen(cmd)as fn:
        k = fn.read()
    return k.splitlines()


def write_shell(cmd, lines):
    '''
    执行系统命令，将指定的文通过管道向该程序输入。
    '''
    with os.popen(cmd, 'w') as fn:
        if isinstance(lines, str):
            fn.write(lines)
        elif isinstance(lines, (tuple, list)):
            [fn.write('%s\n' % (x))for x in lines]


def exec_shell(cmd):
    '''
    执行系统命令。
    '''
    return os.system(cmd)

def wlen(s):
    '''
    用于统计字符串的显示宽度，一个汉字或双字节的标点占两个位，
    单字节的字符占一个字节。
    '''
    return sum([2 if ord(x) > 127 else 1 for x in s])

_des = None


def __get_des():
    from .pyDes import des, PAD_PKCS5
    global _des
    if _des is None:
        _des = des(key='huangtao', padmode=PAD_PKCS5)
    return _des


def encrypt(pwd):
    '''
    可逆加密程序。
    '''
    b = __get_des().encrypt(pwd)
    return "".join(['%02X' % (x)for x in b])


def decrypt(code):
    '''
    解密程序。
    '''
    b = __get_des().decrypt(bytes.fromhex(code))
    return b.decode('utf8')


def get_py(s, style=4, sep=''):
    '''
    获取拼音字母。
    '''
    from pypinyin.core import phrase_pinyin
    return sep.join([x[0] for x in phrase_pinyin(s, style, None)])


class _PY(type):

    def __truediv__(self, s):
        return get_py(s)

    def __or__(self, s):
        return get_py(s, style=0, sep=' ')


class PY(metaclass=_PY):
    '''以一种高逼格的方式获取拼音
    获取拼音首字母：  PY/'我们'   ===>   'wm'
    获取拼音：       PY|'我们'   ===>    'wo men'
    '''
    pass


def split(data, size=1000):
    '''拆分数据，其中datas应为list,size为每批数据的数量'''
    length = len(data)
    i = 0
    for i in range(size, length, size):
        yield data[i - size:i]
    else:
        yield data[i:]


def deprecation(func, replace=''):
    '''DeprecationWarning'''
    import warnings
    message = "%s 已被弃用" % (func)
    if replace:
        message += "，请使用 %s 替代" % (replace)
    warnings.warn(message, DeprecationWarning, stacklevel=2)

generator = type((x for x in 'hello'))
