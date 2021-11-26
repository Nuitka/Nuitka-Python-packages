import nputils
from typing import *

import os
import shutil


def run(temp_dir: str):
    nputils.download_extract("https://zlib.net/zlib1211.zip", temp_dir)

    nputils.setup_compiler_env()

    nputils.auto_patch_MD_MT(os.path.join(temp_dir, "zlib-1.2.11", "win32"))

    os.chdir(os.path.join(temp_dir, "zlib-1.2.11"))

    nputils.nmake("/f", "win32/Makefile.msc")

    nputils.install_dep_libs("zlib", os.path.join(temp_dir, "zlib-1.2.11", "zlib.lib"))
    nputils.install_dep_include("zlib", os.path.join(temp_dir, "zlib-1.2.11", "*.h"))
