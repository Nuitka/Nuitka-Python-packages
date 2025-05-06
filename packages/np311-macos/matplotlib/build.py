import __np__
import glob
import shutil
import sys
import os
import setuptools.build_meta
from tempfile import TemporaryDirectory

import mesonpy

from wheel.wheelfile import WheelFile


def run(wheel_directory):
    __np__.run_with_output("patch", "-t", "-p1", "-i",
                              os.path.join(os.path.dirname(__file__), "matplotlib-static-patch.patch"))

    os.environ["MACOSX_DEPLOYMENT_TARGET"] = "10.9"
    os.environ["CMAKE_PREFIX_PATH"] = __np__.find_dep_root("freetype")
    os.environ["PATH"] = (os.path.dirname(__np__.find_build_tool_exe("cmake", "cmake")) + os.pathsep +
                   os.path.dirname(__np__.find_build_tool_exe("ninja", "ninja")) + os.pathsep + os.environ["PATH"])

    __np__.run_with_output(sys.executable, "-m", "build", "-w", "--no-isolation",
                           "-Csetup-args=-Dsystem-freetype=True")

    wheel_location = glob.glob(os.path.join("dist", "matplotlib-*.whl"))[0]

    wheel_name = os.path.basename(wheel_location)
    shutil.copy(wheel_location, os.path.join(wheel_directory, wheel_name))
    return os.path.join(wheel_directory, wheel_name)
