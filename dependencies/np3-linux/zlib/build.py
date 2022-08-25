import __np__
from typing import *

import os
import sysconfig


def run(temp_dir: str):
    __np__.download_extract("https://github.com/madler/zlib/archive/refs/tags/v1.2.12.zip", temp_dir)

    os.chdir(os.path.join(temp_dir, "zlib-1.2.12"))

    __np__.run_with_output("/bin/bash",
                           "configure",
                           "--prefix=" + __np__.find_dep_root("zlib"),
                           "--static")

    __np__.make()

    __np__.install_dep_libs("zlib", os.path.join(temp_dir, "zlib-1.2.12", "libz.a"))
    __np__.install_dep_include("zlib", os.path.join(temp_dir, "zlib-1.2.12", "*.h"))
