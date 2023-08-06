# -*- coding: utf-8 -*-
import io
import re
import os
import sys
from setuptools import setup, find_packages
from distutils.core import setup

# 约定当前文件所在的父目录名为包名称
PACKAGE_NAME = os.path.basename(os.path.dirname(__file__))


def read(*names, **kwargs):
    return io.open(
        os.path.join(os.path.dirname(__file__), *names),
        encoding=kwargs.get("encoding", "utf8")
    ).read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


# TODO 可以根据需要扩展相关的属性发布到PYPI服务器上分享传播
setup(
    name=PACKAGE_NAME,
    version=find_version('%s/__init__.py' % PACKAGE_NAME),
    packages=find_packages(),
    zip_safe=False,
    license="ISC",
    platforms="Independant",
    # include_package_data=True,
    install_requires=['xbase', ],
)
