import __np__
from typing import *

import os
import shutil
import glob


def run(temp_dir: str):
    # We have to use the git download instead of the official archive since it is missing
    # the file "opus_buildtype.cmake" at time of writing. :(
    __np__.download_extract("https://github.com/xiph/opus/archive/refs/tags/v1.3.1.zip", temp_dir)

    src_dir = glob.glob(os.path.join(temp_dir, "opus*"))[0]

    # We have to write this file manually since it is not included in git.
    with open(os.path.join(src_dir, "package_version"), 'w') as f:
        f.write('PACKAGE_VERSION="1.3.1"\n')

    build_dir = os.path.join(temp_dir, "build")
    os.mkdir(build_dir)
    os.chdir(build_dir)

    os.environ["MACOSX_DEPLOYMENT_TARGET"] = "10.9"
    os.environ["PATH"] = os.path.dirname(__np__.find_build_tool_exe("ninja", "ninja")) + os.pathsep + os.environ["PATH"]
    __np__.run_build_tool_exe("cmake", "cmake", "-G", "Ninja",
                              "-DCMAKE_BUILD_TYPE=Release", src_dir)
    __np__.run_build_tool_exe("ninja", "ninja")

    __np__.install_dep_libs("opus", os.path.join(build_dir, "libopus.a"))
    __np__.install_dep_include("opus", os.path.join(src_dir, "include", "*.h"))
