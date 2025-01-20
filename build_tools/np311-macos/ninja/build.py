import __np__
import glob
from typing import *

import os


def run(temp_dir: str):
    __np__.download_extract("https://github.com/ninja-build/ninja/releases/download/v1.12.1/ninja-mac.zip",
                            temp_dir)
    __np__.install_build_tool("ninja", os.path.join(temp_dir, "*"))
