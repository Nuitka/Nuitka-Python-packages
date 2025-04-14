import __np__
from typing import *

import os
import shutil
import glob

import sysconfig


def run(temp_dir: str):
    # Harfbuzz depends on freetype and freetype depends on harfbuzz. :(
    # We will build freetype first here and then base off that, but we will also have a separate freetype package.
    ft_dir = os.path.join(temp_dir, 'ft')

    __np__.download_extract("https://master.dl.sourceforge.net/project/freetype/freetype2/2.7.1/freetype-2.7.1.tar.gz", ft_dir)

    ft_src_dir = glob.glob(os.path.join(ft_dir, "freetype*"))[0]

    ft_build_dir = os.path.join(ft_dir, "build")
    os.mkdir(ft_build_dir)
    os.chdir(ft_build_dir)

    ft_install_dir = os.path.join(ft_dir, "install")
    os.mkdir(ft_install_dir)

    os.environ["MACOSX_DEPLOYMENT_TARGET"] = "10.9"
    os.environ["PATH"] = os.path.dirname(__np__.find_build_tool_exe("ninja", "ninja")) + os.pathsep + os.environ[
        "PATH"]
    os.environ["CFLAGS"] = sysconfig.get_config_var("CFLAGS")
    __np__.run_build_tool_exe("cmake", "cmake", "-G", "Ninja",
                              "-DCMAKE_BUILD_TYPE=Release",
                              "-DCMAKE_INSTALL_PREFIX=" + ft_install_dir,
                              "-DZLIB_ROOT=" + __np__.find_dep_root("zlib"),
                              "-DWITH_HarfBuzz=OFF", "-DWITH_BZip2=OFF",
                              "-DWITH_PNG=OFF", ft_src_dir)
    __np__.run_build_tool_exe("ninja", "ninja")

    __np__.run_build_tool_exe("ninja", "ninja", "install")

    __np__.download_extract("https://github.com/harfbuzz/harfbuzz/archive/refs/tags/2.6.4.zip", temp_dir)

    src_dir = glob.glob(os.path.join(temp_dir, "harfbuzz*"))[0]
    os.chdir(src_dir)

    build_dir = os.path.join(temp_dir, "build")
    os.mkdir(build_dir)
    os.chdir(build_dir)

    install_dir = os.path.join(temp_dir, "install")
    os.mkdir(install_dir)

    __np__.run_build_tool_exe("cmake", "cmake", "-G", "Ninja",
                              "-DCMAKE_BUILD_TYPE=Release",
                              "-DCMAKE_INSTALL_PREFIX=" + install_dir,
                              "-DCMAKE_PREFIX_PATH=" + ft_install_dir,
                              "-DHB_HAVE_FREETYPE=ON", "-DHB_BUILD_TESTS=OFF",
                              "-DHB_BUILD_UTILS=OFF", "-DHB_BUILD_SUBSET=OFF",
                              "-DHB_HAVE_INTROSPECTION=OFF", "-DHB_HAVE_CORETEXT=OFF",
                              f"-DFREETYPE_INCLUDE_DIR_freetype2={ft_install_dir}/include/freetype2",
                              f"-DFREETYPE_INCLUDE_DIR_ft2build={ft_install_dir}/include/freetype2",
                              src_dir)
    __np__.run_build_tool_exe("ninja", "ninja")

    __np__.run_build_tool_exe("ninja", "ninja", "install")

    __np__.install_dep_libs("harfbuzz", os.path.join(install_dir, "lib", "*.a"))
    __np__.install_dep_include("harfbuzz", os.path.join(install_dir, "include", "harfbuzz", "*.h"))
