#!/usr/bin/env python3
# 项目：克隆github.com上的项目
# 模块：命令行模块
# 作者：黄涛
# License:GPL
# Email:huangtao.sh@icloud.com
# 创建：2015-06-11 12:28
# 修订：2016-11-18 采用Parser来分析参数

#from stdlib import parse_args,exec_shell
from orange import arg, exec_shell
import sys


@arg('repos', nargs='+', metavar='repo', help="要下载的软件仓库，可以为多个")
@arg('-u', '--user', nargs='?', help='要下载的用户名,默认为本人的仓库')
def proc(repos=None, user=None, protocol='SSH'):
    if user is None:
        from configparser import ConfigParser
        import os
        config = ConfigParser()
        config.read([os.path.expanduser('~/.gitconfig')])
        try:
            user = config.get('user', 'name')
        except:
            raise Exception('用户不存在！')
    protocol = protocol.upper()
    URL = 'git@github.com:%s' % (user) if protocol == 'SSH' else \
        'https://github.com/%s' % (user)
    for repo in repos:
        url = '%s/%s.git' % (URL, repo)
        print('cloning', url)
        exec_shell('git clone %s' % (url))


if __name__ == '__main__':
    proc()
