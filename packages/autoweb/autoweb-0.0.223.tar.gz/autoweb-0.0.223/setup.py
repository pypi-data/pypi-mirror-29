# 由于安装脚本会在下载后执行相对路径变化需要这部分更改为动态代码写入配置参数
# 不要修改下面两行打包脚本会自动补上对应的正确值。
# PACKAGE_NAME = 'PACKAGE_NAME'
# PACKAGE_VERSION = 'PACKAGE_VERSION'
PACKAGE_NAME = 'autoweb'
PACKAGE_VERSION = '0.0.223'
import io
import re
import os
import sys
from setuptools import setup, find_packages
from distutils.core import setup
from distutils.command.sdist import sdist
from distutils.command.install_lib import install_lib
from distutils import log
from distutils.dep_util import newer
from py_compile import compile
from types import *
from glob import glob
from warnings import warn
from distutils.core import Command
from distutils import dir_util, dep_util, file_util, archive_util
from distutils.text_file import TextFile
from distutils.errors import *
from distutils.filelist import FileList
from distutils import log
from distutils.util import convert_path


class CmdSdist(sdist):
    # 重写此方法实现字节码编译处理加密打包PIP文件
    def make_release_tree(self, base_dir, files):
        """Create the directory tree that will become the source
        distribution archive.  All directories implied by the filenames in
        'files' are created under 'base_dir', and then we hard link or copy
        (if hard linking is unavailable) those files into place.
        Essentially, this duplicates the developer's source tree, but in a
        directory named after the distribution, containing only the files
        to be distributed.
        """
        # Create all the directories under 'base_dir' necessary to
        # put 'files' there; the 'mkpath()' is just so we don't die
        # if the manifest happens to be empty.
        self.mkpath(base_dir)
        dir_util.create_tree(base_dir, files, dry_run=self.dry_run)

        # And walk over the list of files, either making a hard link (if
        # os.link exists) to each one that doesn't already exist in its
        # corresponding location under 'base_dir', or copying each file
        # that's out-of-date in 'base_dir'.  (Usually, all files will be
        # out-of-date, because by default we blow away 'base_dir' when
        # we're done making the distribution archives.)

        if hasattr(os, 'link'):  # can make hard links on this system
            link = 'hard'
            msg = "making hard links in %s..." % base_dir
        else:  # nope, have to copy
            link = None
            msg = "copying files to %s..." % base_dir

        if not files:
            log.warn("no files to distribute -- empty manifest?")
        else:
            log.info(msg)
        for file in files:
            if not os.path.isfile(file):
                log.warn("'%s' not a regular file -- skipping", file)
            else:
                dest = os.path.join(base_dir, file)
                self.copy_file(file, dest, link=link)
                # 代码优化改进点在拷贝源代码打包的时候将py文件编译为pyc并且删除py源文件
                from py_compile import compile
                import re
                matchs = re.match(r"^(.+)(\.py)$", dest)
                if matchs is not None:
                    if re.match(r".*-\d+.\d+.\d+\/setup\.py$", dest) is not None:
                        print('ignore setup.py compile which is needed by install process')
                        continue
                    with open(dest,'r+') as f:
                        f.write('')
                        f.flush()
                    # os.unlink(dest) # 只保留空源代码方便安装复制
                    compile(dest, matchs.group(1) + '.pyc')


        self.distribution.metadata.write_pkg_info(base_dir)


class CmdInstallLib(install_lib):
    # def install(self):
    #     for root, dirs, files in os.walk(self.build_dir):
    #         current = root.replace(self.build_dir, self.install_dir)
    #         for i in dirs:
    #             self.mkpath(os.path.join(current, i))
    #         for i in files:
    #             file = os.path.join(root, i)
    #             cfile = os.path.join(current, i) + "c"
    #             cfile_base = os.path.basename(cfile)
    #             if self.force or newer(file, cfile):
    #                 log.info("byte-compiling %s to %s", file, cfile_base)
    #                 compile(file, cfile)
    #             else:
    #                 log.debug("skipping byte-compilation of %s", file)

    def run(self):
        self.build()
        outfiles = self.install()
        # 安装完成后删除空源代码文件
        if outfiles is not None and self.distribution.has_pure_modules():
            self.byte_compile(outfiles)
            for i in outfiles:
                os.unlink(i)

setup(
    cmdclass={"sdist": CmdSdist, "install_lib": CmdInstallLib},
    name=PACKAGE_NAME,
    version=PACKAGE_VERSION,
    packages=find_packages(),
    zip_safe=True,
    license="ISC",
    platforms="Independant",
)
