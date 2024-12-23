import __np__
import glob
from typing import *

import os


def run(temp_dir: str):
    # It seems that miniconda is the only way to get prebuilt binaries for flang on windows :(
    # Revisit this when LLVM finally decides to publish windows binaries for flang.
    __np__.run_build_tool_exe("miniconda", "conda.exe", "create", "--prefix=" + temp_dir, "-y",
                              "flang", "perl", "libflang")

    __np__.install_build_tool("flang", os.path.join(temp_dir, "Library", "*"))
