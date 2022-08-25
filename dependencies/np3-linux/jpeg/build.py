import __np__
from typing import *

import os
import shutil
import glob


def run(temp_dir: str):
    __np__.download_extract("https://ijg.org/files/jpegsr9d.zip", temp_dir)

    src_dir = glob.glob(os.path.join(temp_dir, "jpeg*"))[0]
    os.chdir(src_dir)

    os.environ["PATH"] = os.path.dirname(__np__.find_build_tool_exe("ninja", "ninja")) + os.pathsep + os.environ["PATH"]
    shutil.copy(os.path.join(temp_dir, "libjpeg.cmake"), os.path.join(src_dir, "CMakeLists.txt"))
    shutil.copy(os.path.join(temp_dir, "libjpeg-jconfig.h.cmake"), os.path.join(src_dir, "jconfig.h.cmake"))

    build_dir = os.path.join(temp_dir, "build")
    os.mkdir(build_dir)
    os.chdir(build_dir)

    __np__.run_build_tool_exe("cmake", "cmake", "-G", "Ninja",
                              "-DCMAKE_BUILD_TYPE=Release", src_dir)
    __np__.run_build_tool_exe("ninja", "ninja")

    __np__.install_dep_libs("jpeg", os.path.join(build_dir, "*.a"))
    __np__.install_dep_include("jpeg", os.path.join(src_dir, "*.h"))
    __np__.install_dep_include("jpeg", os.path.join(build_dir, "*.h"))
