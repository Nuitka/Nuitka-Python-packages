import __np__
from typing import *

import os
import sys
import shutil
import glob
import sysconfig


def run(temp_dir: str):
    __np__.download_extract("https://www.panda3d.org/download/panda3d-1.10.11/panda3d-1.10.11-tools-mac.tar.gz", temp_dir)

    __np__.install_dep_libs("nvidiacg", os.path.join(temp_dir, "panda3d-1.10.11/thirdparty/darwin-libs-a/nvidiacg", "lib", "*.dylib"))
    __np__.install_files(os.path.dirname(os.path.realpath(sys.executable)), os.path.join(temp_dir, "panda3d-1.10.11/thirdparty/darwin-libs-a/nvidiacg", "lib", "*.dylib"))
    __np__.install_files(os.path.join(os.path.dirname(os.path.realpath(sys.executable)), "..", "lib"),
                         os.path.join(temp_dir, "panda3d-1.10.11/thirdparty/darwin-libs-a/nvidiacg", "lib", "*.dylib"))
    # We must also install the proprietary DLLs. :(
    __np__.install_dep_include("nvidiacg", os.path.join(temp_dir, "panda3d-1.10.11/thirdparty/darwin-libs-a/nvidiacg", "include", "*"))
