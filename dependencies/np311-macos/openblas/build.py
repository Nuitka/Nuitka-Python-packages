import __np__
from typing import *

import os
import shutil
import glob


def run(temp_dir: str):
    __np__.download_extract("https://github.com/OpenMathLib/OpenBLAS/releases/download/v0.3.28/OpenBLAS-0.3.28.zip", temp_dir)

    src_dir = glob.glob(os.path.join(temp_dir, "OpenBLAS*"))[0]

    install_dir = os.path.join(temp_dir, "install")
    os.mkdir(install_dir)
    build_dir = os.path.join(temp_dir, "build")
    os.mkdir(build_dir)
    os.chdir(build_dir)

    env = os.environ.copy()
    env["MACOSX_DEPLOYMENT_TARGET"] = "10.9"
    __np__.run_build_tool_exe("cmake", "cmake", "-DCMAKE_BUILD_TYPE=Release",
                              "-DCMAKE_INSTALL_PREFIX=" + install_dir, "-DBUILD_STATIC_LIBS=ON", "-DBUILD_SHARED_LIBS=OFF",
                              "-DBUILD_TESTING=OFF", src_dir, env=env)
    __np__.run_with_output("make", "-j4", "install", env=env)

    __np__.install_dep_libs("openblas", os.path.join(install_dir, "lib", "*"),
                            base_dir=os.path.join(install_dir, "lib"))
    __np__.install_dep_include("openblas", os.path.join(install_dir, "include", "*"),
                               base_dir=os.path.join(install_dir, "include"))
