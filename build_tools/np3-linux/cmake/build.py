import __np__
from typing import *

import os


def run(temp_dir: str):
    __np__.download_extract("https://github.com/Kitware/CMake/releases/download/v3.24.1/cmake-3.24.1-linux-x86_64.tar.gz", temp_dir)
    __np__.install_build_tool("cmake", os.path.join(temp_dir, "cmake-3.24.1-linux-x86_64", "*"))
