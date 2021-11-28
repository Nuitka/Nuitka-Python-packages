import __np__
from typing import *

import os
import shutil
import glob


def run(temp_dir: str):
    __np__.download_extract("https://github.com/bulletphysics/bullet3/archive/2fb92bc40c16e4da5a9018479d4a8e1899702ab8.zip", temp_dir)

    __np__.setup_compiler_env()

    src_dir = glob.glob(os.path.join(temp_dir, "bullet*"))[0]

    build_dir = os.path.join(temp_dir, "build")
    os.mkdir(build_dir)
    os.chdir(build_dir)

    os.environ["PATH"] = os.path.dirname(__np__.find_build_tool_exe("ninja", "ninja.exe")) + os.pathsep + os.environ["PATH"]
    __np__.run_build_tool_exe("cmake", "cmake.exe", "-G", "Ninja",
                              "-DCMAKE_BUILD_TYPE=Release", "-DBUILD_CPU_DEMOS=OFF",
                              "-DBUILD_OPENGL3_DEMOS=OFF", "-DBUILD_UNIT_TESTS=OFF",
                              src_dir)
    __np__.run_build_tool_exe("ninja", "ninja.exe")

    __np__.install_dep_libs("bullet", os.path.join(build_dir, "lib", "*.lib"))
    __np__.install_dep_include("bullet", os.path.join(src_dir, "src", "**", "*.h"), base_dir=os.path.join(src_dir, "src"))
    __np__.install_dep_include("bullet", os.path.join(src_dir, "src", "*.h"), base_dir=os.path.join(src_dir, "src"))
