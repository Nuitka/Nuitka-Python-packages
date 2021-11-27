import __np__
from typing import *

import os
import shutil
import glob


def run(temp_dir: str):
    __np__.download_extract("https://github.com/harfbuzz/harfbuzz/archive/refs/tags/3.1.2.zip", temp_dir)

    __np__.setup_compiler_env()

    src_dir = glob.glob(os.path.join(temp_dir, "harfbuzz*"))[0]

    build_dir = os.path.join(temp_dir, "build")
    os.mkdir(build_dir)
    os.chdir(src_dir)

    os.environ["CFLAGS"] = "/MT"
    os.environ["CXXFLAGS"] = "/MT"
    os.environ["PATH"] = os.path.dirname(__np__.find_build_tool_exe("ninja", "ninja.exe")) + os.pathsep + os.environ["PATH"]
    __np__.run_build_tool_exe("meson", "meson.exe", "--buildtype=plain", "--default-library=static", "build")
    __np__.run_build_tool_exe("ninja", "ninja.exe", "-Cbuild", "-v")

    os.rename(os.path.join(src_dir, "build", "src", "libharfbuzz.a"), os.path.join(src_dir, "build", "src", "harfbuzz.lib"))
    os.rename(os.path.join(src_dir, "build", "src", "libharfbuzz-subset.a"), os.path.join(src_dir, "build", "src", "harfbuzz-subset.lib"))
    __np__.install_dep_libs("harfbuzz", os.path.join(src_dir, "build", "src", "*.lib"))
    __np__.install_dep_include("harfbuzz", os.path.join(src_dir, "src", "*.h"))
    __np__.install_dep_include("harfbuzz", os.path.join(src_dir, "build", "src", "*.h"))
