import __np__
from typing import *

import os
import shutil
import glob


def run(temp_dir: str):
    __np__.download_extract("https://github.com/xiph/ogg/releases/download/v1.3.5/libogg-1.3.5.zip", temp_dir)

    src_dir = glob.glob(os.path.join(temp_dir, "libogg*"))[0]

    build_dir = os.path.join(temp_dir, "build")
    os.mkdir(build_dir)
    os.chdir(build_dir)

    os.environ["MACOSX_DEPLOYMENT_TARGET"] = "10.9"
    os.environ["PATH"] = os.path.dirname(__np__.find_build_tool_exe("ninja", "ninja")) + os.pathsep + os.environ["PATH"]
    __np__.run_build_tool_exe("cmake", "cmake", "-G", "Ninja",
                              "-DCMAKE_BUILD_TYPE=Release", src_dir)
    __np__.run_build_tool_exe("ninja", "ninja")

    __np__.install_dep_libs("ogg", os.path.join(build_dir, "libogg.a"))
    __np__.install_dep_include("ogg", os.path.join(src_dir, "include", "**", "*.h"),
                               base_dir=os.path.join(src_dir, "include"))
    __np__.install_dep_include("ogg", os.path.join(build_dir, "include", "*"))
