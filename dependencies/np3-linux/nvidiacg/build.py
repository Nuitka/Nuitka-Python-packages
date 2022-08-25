import __np__
from typing import *

import os
import shutil
import glob
import sysconfig


def run(temp_dir: str):
    __np__.download_extract("http://deb.debian.org/debian/pool/non-free/n/nvidia-cg-toolkit/nvidia-cg-toolkit_3.1.0013.orig-amd64.tar.gz", temp_dir)

    __np__.install_dep_libs("nvidiacg", os.path.join(temp_dir, "usr", "lib64", "*.so"))
    # We must also install the proprietary DLLs. :(
    __np__.install_dep_include("nvidiacg", os.path.join(temp_dir, "usr", "include", "*"))
