# -*- coding: utf-8 -*-
import io
import re
import os
from setuptools import setup, find_packages
from distutils.core import setup
from distutils.command.install_lib import install_lib
from distutils.command.build_py import build_py
from distutils.command.sdist import sdist
from distutils import log
from distutils.dep_util import newer
from py_compile import compile

# 约定当前文件所在的父目录名为包名称
# PACKAGE_NAME = os.path.basename(os.path.dirname(__file__))
PACKAGE_NAME = 'autoweb'


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


# 自定义扩展easy_install的方法（将python源代码编译为字节码并且删除掉源码后进行egg打包发布）
class InstallLib(install_lib):
    def install(self):
        for root, dirs, files in os.walk(self.build_dir):
            current = root.replace(self.build_dir, self.install_dir)
            for i in dirs:
                self.mkpath(os.path.join(current, i))

            for i in files:
                file = os.path.join(root, i)
                cfile = os.path.join(current, i) + "c"
                cfile_base = os.path.basename(cfile)
                if self.force or newer(file, cfile):
                    log.info("byte-compiling %s to %s", file, cfile_base)
                    compile(file, cfile)
                else:
                    log.debug("skipping byte-compilation of %s", file)

    def run(self):
        self.build()
        outfiles = self.install()
        if outfiles is not None and self.distribution.has_pure_modules():
            self.byte_compile(outfiles)
            for i in outfiles:
                os.unlink(i)


setup(
    # cmdclass={"install_lib": InstallLib},
    name=PACKAGE_NAME,
    version=find_version('%s/__init__.py' % PACKAGE_NAME),
    packages=find_packages(),
    zip_safe=True,
    license="ISC",
    platforms="Independant",
)
