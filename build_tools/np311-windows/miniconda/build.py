import __np__
import glob
from typing import *

import os


def run(temp_dir: str):
    downloaded_file = __np__.download_file(
        "https://repo.anaconda.com/miniconda/Miniconda3-py311_24.11.1-0-Windows-x86_64.exe", temp_dir)

    os.chdir(temp_dir)
    install_dir = os.path.join(temp_dir, "install")
    os.mkdir(install_dir)
    __np__.run_with_output(downloaded_file, "/InstallationType=JustMe", "/AddToPath=0", "/S", "/RegisterPython=0",
                           "/NoRegistry=1", "/NoScripts=1", "/NoShortcuts=1", "/D=" + install_dir)
    os.rename(os.path.join(install_dir, "_conda.exe"), os.path.join(install_dir, "conda.exe"))
    __np__.install_build_tool("miniconda", os.path.join(install_dir, "*"))
