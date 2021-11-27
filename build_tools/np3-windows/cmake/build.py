import __np__
from typing import *

import os


def run(temp_dir: str):
    __np__.download_extract("https://github.com/Kitware/CMake/releases/download/v3.21.0/cmake-3.21.0-windows-i386.zip", temp_dir)
    __np__.install_build_tool("cmake", os.path.join(temp_dir, "cmake-3.21.0-windows-i386", "*"))
