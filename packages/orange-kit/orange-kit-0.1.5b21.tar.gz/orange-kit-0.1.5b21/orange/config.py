# 项目：标准库函数模块
# 模块：配置程序
# 作者：黄涛
# License:GPL
# Email:huangtao.sh@icloud.com
# 创建：2015-05-26 16:12
# 修订：2016-10-28 增加

import os
import sys
import sysconfig
import orange
import atexit
from configparser import ConfigParser
from orange import decrypt, encrypt, Path


class Config:
    def __init__(self, config_path=None, data_path=None,
                 is_dev=None, project=None):
        if is_dev is None:
            self.is_dev = orange.is_dev()
        else:
            self.is_dev = is_dev
        if project is None:
            self.project = os.path.splitext(
                os.path.basename(sys.argv[0]))[0]
        else:
            self.project = project
        self.os_name = os.name
        if self.os_name == 'posix':
            config_ext = '.conf'
            self.config_path = os.path.expanduser(
                "~/.%s" % (self.project))
        else:
            config_ext = '.ini'
            self.config_path = os.path.join(os.getenv("APPDATA"),
                                            self.project)
        if self.is_dev:
            self.config_path = os.path.abspath("appdata")
        else:
            if config_path:
                self.config_path = config_path
        if not hasattr(self, "data_path"):
            self.data_path = self.config_path
        self.config_file = os.path.join(self.data_path,
                                        self.project+config_ext)
        self.modified = False
        self.load_config()

    def load_config(self, files=None):
        if files is None:
            files = self.config_file
        if not hasattr(self, 'parser'):
            self.parser = ConfigParser()
        self.parser.clear()
        self.parser.read(files, encoding='utf8')
        self.modified = False
        if isinstance(files, str):
            self.cur_file = files
        else:
            self.cur_file = files[-1]

    def __setitem__(self, name, data):
        return self.update(name, data)

    @property
    def sections(self):
        return self.parser.sections()

    def get(self, section):
        if self.parser.has_section(section):
            d = {}
            for option, value in self.parser.items(section):
                if self.is_passwd(option):
                    value = decrypt(value)
                d[option] = value
            return d

    def update(self, section, data):
        self.modified = True
        if not self.parser.has_section(section):
            self.parser.add_section(section)
        for option, value in data.items():
            if self.is_passwd(option):
                value = encrypt(value)
            self.parser.set(section, option, str(value))

    def get_many(self, *sections):
        return dict([(section, self.get(section)) for section in sections])

    def update_many(self, datas):
        for section, data in datas.items():
            self.update(section, data)

    def is_passwd(self, key):
        return key.lower() in ('passwd', 'password')

    def save_config(self):
        # ensure_path(os.path.dirname(self.cur_file))
        Path(self.cur_file).parent.ensure()
        if self.modified:
            with open(self.cur_file, 'w', encoding='utf8')as fn:
                self.parser.write(fn)

    def init_logging(self):
        import logging
        file_name = os.path.join(self.data_path,
                                 self.project+'.log')
        if self.is_dev:
            level = 'DEBUG'
        else:
            level = 'WARN'
        default = {
            'filename': file_name,
            'level': level,
            'format': '%(asctime)s %(levelname)s\t%(message)s',
            'datefmt': '%Y-%m-%d %H:%M'}
        default.update(self.get('logging'))
        logging.basicConfig(**default)


_config = None


def config(*args, **kw):
    global _config
    if _config is None:
        _config = Config(*args, **kw)
    return _config


@atexit.register
def save_config():
    if _config and _config.modified:
        _config.save_config()
