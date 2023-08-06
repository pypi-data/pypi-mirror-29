# 项目：标准库函数
# 模块：macos的plist生成器
# 作者：黄涛
# License:GPL
# Email:huangtao.sh@icloud.com
# 创建：2016-09-06 23:27
# 修改：2016-9-17 使用plistlib 来写入plist文件

import sys
from plistlib import *
from orange import *
import sys

def proc(filename,label,*args):
    filename=str(Path(filename).with_suffix('.plist'))
    with open(filename,'wb') as fn:
        dump(Dict(Label=label,
                  KeepAlive=True,
                  ProgramArguments=args),fn)

def main():
    args=sys.argv
    if len(args)<4:
        print('Usage:\n'
        '\t%s plist-file-name label program args'%(args[0]))
    else:
        proc(*args[1:])
    

if __name__=='__main__':
    main()
