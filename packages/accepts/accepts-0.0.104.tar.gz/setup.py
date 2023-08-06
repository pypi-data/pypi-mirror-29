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


def read_configuration(path):
    # setuptools.config.read_configuration read metadata/options ONLY
    result = dict()
    config = ConfigParser()
    config.read(path)
    for section in config.sections():
        for key, val in config.items(section):
            if val and val[0] == "\n":  # array (first line empty)
                val = list(filter(None, val.splitlines()))
            # 1) Python 2.x ConfigParser stripping blank lines in multiline value
            # 2) ConfigParser breaks tab/space indentation (use README.rst)
            if key == "description-file":  # ./README.rst
                key = "long_description"
                try:
                    val = open(val).read()
                except:
                    pass
            result[key] = val
    return result


path = __file__.replace("setup.py", "setup.cfg")
setup_cfg_data = read_configuration(path)
setup(**setup_cfg_data)
