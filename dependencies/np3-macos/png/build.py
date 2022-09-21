import __np__
from typing import *

import os
import shutil
import glob


def run(temp_dir: str):
    __np__.download_extract("http://prdownloads.sourceforge.net/libpng/libpng-1.6.37.tar.xz?download", temp_dir)

    src_dir = glob.glob(os.path.join(temp_dir, "libpng*"))[0]

    build_dir = os.path.join(temp_dir, "build")
    os.mkdir(build_dir)
    os.chdir(build_dir)

    os.environ["MACOSX_DEPLOYMENT_TARGET"] = "10.9"
    os.environ["PATH"] = os.path.dirname(__np__.find_build_tool_exe("ninja", "ninja")) + os.pathsep + os.environ["PATH"]
    __np__.run_build_tool_exe("cmake", "cmake", "-G", "Ninja",
                              "-DCMAKE_BUILD_TYPE=Release",
                              "-DPNG_SHARED=OFF", "-DPNG_TESTS=OFF",
                              "-DZLIB_LIBRARY=" + os.path.join(__np__.find_dep_libs("zlib"), "libz.a"),
                              "-DZLIB_INCLUDE_DIR=" + __np__.find_dep_include("zlib"),
                              src_dir)
    __np__.run_build_tool_exe("ninja", "ninja")

    __np__.install_dep_libs("png", os.path.join(build_dir, "*.a"))
    __np__.install_dep_include("png", os.path.join(src_dir, "*.h"), base_dir=os.path.join(src_dir, "include"))
    __np__.install_dep_include("png", os.path.join(build_dir, "*.h"))
