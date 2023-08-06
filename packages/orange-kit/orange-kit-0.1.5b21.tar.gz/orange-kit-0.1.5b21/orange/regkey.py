# 项目：标准库函数
# 模块：Windows注册表读写模块
# 作者：黄涛
# License:GPL
# Email:huangtao.sh@icloud.com
# 创建：2017-03-15 20:35

# 警告：
#     编写跨平台程序时，不要直接引用本模块，正确的写法如下：
#     if os.name=='nt':
#         import regkey
#       


from winreg import *

__all__='RegKey','HKLM','HKCU','HKU','REG_BINARY',\
        'REG_DWORD','REG_EXPAND_SZ','REG_SZ','add_path'

class RegKey(object):
    __slots__='_items','_key','_subkey'
    def __init__(self,key,subkey=None):
        self._items={}
        self._key=key
        self._subkey=subkey
        
    def open(self):
        if self._subkey:
            subkey=self._subkey.replace('/','\\')
            self._key=CreateKey(self._key,subkey)
            self._subkey=None
        return self

    __enter__=open
        
    def __truediv__(self,subkey):
        if self._subkey:
            # 未打开的返回自身
            self._subkey='%s\\%s'%(self._subkey,subkey)
            return self
        else:
            # 已调用open
            return RegKey(self._key,subkey)

    def close(self):
        if hasattr(self._key,'Close'):
            self._key.Close()
    
    def __exit__(self,*args):
        self.close()

    def __getitem__(self,name):
        if name not in self._items:
            try:
                val=QueryValueEx(self._key,name)
            except:
                val=None,None
            self._items[name]=val
        return self._items.get(name)

    @property
    def value(self):
        return QueryValue(self._key,None)

    @value.setter
    def value(self,val):
        return SetValue(self._key,REG_SZ,val)
        
    def __setitem__(self,name,value):
        # thd value is tuplie or list: value,type
        if isinstance(value,(tuple,list))and len(value)==2:
            if SetValueEx(self._key,name,0,*reversed(value)):
                self._items[name]=value
        else:
            raise Exception('参数格式不正确，应为value,Type')

    def __delitem__(self,name):
        DeleteValue(self._key,name)

    def iter_keys(self,func=EnumKey):
        i=0
        try:
            while 1:
                yield func(self._key,i)
                i+=1
        except:
            pass

    def iter_values(self):
        return self.iter_keys(func=EnumValue)

HKLM=RegKey(HKEY_LOCAL_MACHINE)
HKCU=RegKey(HKEY_CURRENT_USER)
HKU=RegKey(HKEY_USERS)

def add_path(path,replace=None):
    with HKLM/r'SYSTEM\CurrentControlSet\Control\Session Manager\Environment' as key:
        value,type_=key['Path']
        if replace:
            value=[x for x in value.split(';') if replace not in x]
            value=';'.join(value)
        value='%s;%s'%(value,path)
        key['Path']=value,type_
        
            
