import __np__
from typing import *

import os


def run(temp_dir: str):
    downloaded_file = __np__.download_file("https://github.com/mesonbuild/meson/releases/download/1.5.1/meson-1.5.1-64.msi", temp_dir)
    os.chdir(temp_dir)
    __np__.run_build_tool_exe("lessmsi", "lessmsi.exe", "x", downloaded_file)
    __np__.install_build_tool("meson", os.path.join(temp_dir, "meson-1.5.1-64", "SourceDir", "Meson", "*"))
