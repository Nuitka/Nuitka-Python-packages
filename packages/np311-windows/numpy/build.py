import __np__
import glob
import shutil
import sys
import os
import setuptools.build_meta


def run(wheel_directory):
    __np__.setup_compiler_env()

    __np__.run_build_tool_exe("patch", "patch.exe", "-p1", "-i",
                              os.path.join(os.path.dirname(__file__), "numpy-static-patch.patch"))

    __np__.filter_paths_containing("gfortran.exe")
    env = os.environ.copy()
    env["PEP517_BACKEND_PATH"] = os.pathsep.join([x for x in sys.path if not x.endswith(os.path.sep + "site")])
    env["PATH"] = os.path.dirname(__np__.find_build_tool_exe("ninja", "ninja.exe")) + os.pathsep + env["PATH"]
    env["LIB"] = env["LIB"] + os.pathsep + __np__.find_dep_libs("openblas")
    env["INCLUDE"] = env["INCLUDE"] + os.pathsep + __np__.find_dep_include("openblas")
    __np__.run(sys.executable, "-m", "pip", "wheel", ".", "--verbose", "--no-build-isolation",
               "-Csetup-args=-Dblas=openblas", "-Csetup-args=-Dlapack=openblas", env=env)

    wheel_location = glob.glob("numpy-*.whl")[0]
    wheel_name = os.path.basename(wheel_location)
    shutil.copy(wheel_location, os.path.join(wheel_directory, wheel_name))
    return os.path.join(wheel_directory, wheel_name)
