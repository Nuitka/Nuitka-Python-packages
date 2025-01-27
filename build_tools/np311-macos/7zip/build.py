import __np__
import glob
from typing import *

import os


def run(temp_dir: str):
    __np__.download_extract(
        "https://7-zip.org/a/7z2409-mac.tar.xz", temp_dir)

    os.chdir(temp_dir)
    __np__.install_build_tool("7zip", os.path.join(temp_dir, "7zz"))
