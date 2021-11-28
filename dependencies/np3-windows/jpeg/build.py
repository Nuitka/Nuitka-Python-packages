import __np__
from typing import *

import os
import shutil
import glob


def run(temp_dir: str):
    __np__.download_extract("https://ijg.org/files/jpegsr9d.zip", temp_dir)

    __np__.setup_compiler_env()

    src_dir = glob.glob(os.path.join(temp_dir, "jpeg*"))[0]
    os.chdir(src_dir)

    os.environ["PATH"] = os.path.dirname(__np__.find_build_tool_exe("ninja", "ninja.exe")) + os.pathsep + os.environ["PATH"]
    shutil.copy(os.path.join(temp_dir, "libjpeg.cmake"), os.path.join(src_dir, "CMakeLists.txt"))
    shutil.copy(os.path.join(temp_dir, "libjpeg-jconfig.h.cmake"), os.path.join(src_dir, "jconfig.h.cmake"))

    __np__.auto_patch_MD_MT(src_dir)

    build_dir = os.path.join(temp_dir, "build")
    os.mkdir(build_dir)
    os.chdir(build_dir)

    __np__.run_build_tool_exe("cmake", "cmake.exe", "-G", "Ninja",
                              "-DCMAKE_BUILD_TYPE=Release",
                              "-DCMAKE_MSVC_RUNTIME_LIBRARY=MultiThreaded", src_dir)
    __np__.run_build_tool_exe("ninja", "ninja.exe")

    shutil.copy(os.path.join(build_dir, "jpeg-static.lib"), os.path.join(build_dir, "jpeg.lib"))
    __np__.install_dep_libs("jpeg", os.path.join(build_dir, "*.lib"))
    __np__.install_dep_include("jpeg", os.path.join(src_dir, "*.h"))
    __np__.install_dep_include("jpeg", os.path.join(build_dir, "*.h"))
