import __np__
from typing import *

import os
import shutil
import glob


def run(temp_dir: str):
    __np__.download_extract("http://download-mirror.savannah.gnu.org/releases/freetype/freetype-2.11.0.tar.gz", temp_dir)

    __np__.setup_compiler_env()

    src_dir = glob.glob(os.path.join(temp_dir, "freetype*"))[0]

    build_dir = os.path.join(temp_dir, "build")
    os.mkdir(build_dir)
    os.chdir(build_dir)

    os.environ["PATH"] = os.path.dirname(__np__.find_build_tool_exe("ninja", "ninja.exe")) + os.pathsep + os.environ["PATH"]
    __np__.run_build_tool_exe("cmake", "cmake.exe", "-G", "Ninja",
                              "-DCMAKE_BUILD_TYPE=Release", src_dir)
    __np__.run_build_tool_exe("ninja", "ninja.exe")

    __np__.install_dep_libs("freetype", os.path.join(build_dir, "freetype.lib"))
    __np__.install_dep_include("freetype", os.path.join(src_dir, "include", "*"))
    __np__.install_dep_include("freetype", os.path.join(build_dir, "include", "*"))
