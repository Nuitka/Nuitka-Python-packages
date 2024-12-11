import __np__
import glob
import shutil
import sys
import os
import setuptools.build_meta


def run(wheel_directory):
    __np__.setup_compiler_env()

    __np__.run_build_tool_exe("patch", "patch.exe", "-t", "-p1", "-i",
                              os.path.join(os.path.dirname(__file__), "meson-static-patch.patch"))

    return setuptools.build_meta.build_wheel(wheel_directory)
