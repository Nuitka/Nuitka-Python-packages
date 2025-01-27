import __np__
import glob
import shutil
import sys
import os
import setuptools.build_meta


def run(wheel_directory):
    __np__.run_with_output("patch", "-p1", "-i",
                              os.path.join(os.path.dirname(__file__), "numpy-static-patch.patch"))

    env = os.environ.copy()
    env["MACOSX_DEPLOYMENT_TARGET"] = "10.9"
    env["PEP517_BACKEND_PATH"] = os.pathsep.join([x for x in sys.path if not x.endswith(os.path.sep + "site")])
    env["PATH"] = (os.path.dirname(__np__.find_build_tool_exe("cmake", "cmake")) + os.pathsep + 
                   os.path.dirname(__np__.find_build_tool_exe("ninja", "ninja")) + os.pathsep + os.environ["PATH"])
    env["FC"] = __np__.find_build_tool_exe("clang", "flang-new")
    env["LIB"] = os.pathsep + __np__.find_dep_libs("openblas")
    env["INCLUDE"] = os.pathsep + __np__.find_dep_include("openblas")
    env["CMAKE_PREFIX_PATH"] = __np__.find_dep_root("openblas")
    __np__.run(sys.executable, "-m", "pip", "wheel", ".", "--verbose", "--no-build-isolation",
               "-Csetup-args=-Dblas=openblas", "-Csetup-args=-Dlapack=openblas", env=env)

    wheel_location = glob.glob("numpy-*.whl")[0]
    wheel_name = os.path.basename(wheel_location)
    shutil.copy(wheel_location, os.path.join(wheel_directory, wheel_name))
    return os.path.join(wheel_directory, wheel_name)
