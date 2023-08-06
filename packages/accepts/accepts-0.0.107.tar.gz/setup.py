#!/usr/bin/env python
from distutils.core import setup  # Python Standard Library
# pypi.org/project/setuptools/ (python3.2 not supported)
# setup.cfg support: setuptools 30.3.0+
try:
    from configparser import ConfigParser  # python 3+
except ImportError:
    from ConfigParser import ConfigParser  # python 2.x

# ~/.pydistutils.cfg
# path/to/project/README.rst
# path/to/project/setup.cfg
# path/to/project/setup.py


def get_item(key, value):
    if value and value[0] == "\n":  # array (first line empty)
        value = list(filter(None, value.splitlines()))
    # 1) Python 2.x ConfigParser stripping blank lines in multiline value
    # 2) ConfigParser breaks tab/space indentation (use README.rst)
    if key == "description-file":  # ./README.rst
        key = "long_description"
        try:
            value = open(value).read()
        except:
            value = None
    return key, value


def read_configuration(path):
    config = ConfigParser()
    config.read(path)
    result = dict()
    for section in config.sections():
        for key, value in config.items(section):
            key, value = get_item(key, value)
            result[key] = value
    return result


path = __file__.replace("setup.py", "setup.cfg")
setup_cfg_data = read_configuration(path)
setup(**setup_cfg_data)
