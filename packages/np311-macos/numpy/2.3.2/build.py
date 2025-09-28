import __np__
import glob
import shutil
import sys
import os
import setuptools.build_meta
from tempfile import TemporaryDirectory
from wheel.wheelfile import WheelFile


def run(wheel_directory):
    __np__.run_with_output("patch", "-p1", "-i",
                              os.path.join(os.path.dirname(__file__), "numpy-static-patch.patch"))

    build_dir = os.getcwd()

    env = os.environ.copy()
    env["MACOSX_DEPLOYMENT_TARGET"] = "10.9"
    env["PEP517_BACKEND_PATH"] = os.pathsep.join([x for x in sys.path if not x.endswith(os.path.sep + "site")])
    env["PATH"] = (os.path.dirname(__np__.find_build_tool_exe("cmake", "cmake")) + os.pathsep + 
                   os.path.dirname(__np__.find_build_tool_exe("ninja", "ninja")) + os.pathsep + os.environ["PATH"])
    env["FC"] = __np__.find_build_tool_exe("gcc", "gfortran-nuitka")
    env["LIB"] = os.pathsep + __np__.find_dep_libs("openblas")
    env["INCLUDE"] = os.pathsep + __np__.find_dep_include("openblas")
    env["CMAKE_PREFIX_PATH"] = __np__.find_dep_root("openblas")
    env["FFLAGS"] = "-static-libgcc"
    env["PKG_CONFIG"] = "/disabled"
    __np__.run(sys.executable, "-m", "build", "-w", "--no-isolation",
               "-Csetup-args=-Dblas=openblas", "-Csetup-args=-Dlapack=openblas", env=env)

    wheel_location = glob.glob(os.path.join("dist", "numpy-*.whl"))[0]

    wheel_files = []
    with TemporaryDirectory() as tmpdir:
        with WheelFile(wheel_location) as wf:
            for filename in wf.namelist():
                wheel_files.append(filename)
                wf.extract(filename, tmpdir)

        os.chdir(tmpdir)
        __np__.run_with_output("patch", "-p1", "-f", "-i",
                               os.path.join(os.path.dirname(__file__), "numpy-post.patch"))
        os.chdir(build_dir)

        __np__.rename_symbols_in_file(os.path.join(tmpdir, "numpy/random/_sfc64.nuitkapython-311-darwin.a"), "numpy_random__sfc64_")
        __np__.rename_symbols_in_file(os.path.join(tmpdir, "numpy/random/_generator.nuitkapython-311-darwin.a"), "numpy_random__generator_")
        __np__.rename_symbols_in_file(os.path.join(tmpdir, "numpy/random/_mt19937.nuitkapython-311-darwin.a"), "numpy_random__mt19937_")
        __np__.rename_symbols_in_file(os.path.join(tmpdir, "numpy/random/mtrand.nuitkapython-311-darwin.a"), "numpy_random_mtrand_")
        __np__.rename_symbols_in_file(os.path.join(tmpdir, "numpy/random/bit_generator.nuitkapython-311-darwin.a"), "numpy_random_bit_generator_")
        __np__.rename_symbols_in_file(os.path.join(tmpdir, "numpy/random/_philox.nuitkapython-311-darwin.a"), "numpy_random__philox_")
        __np__.rename_symbols_in_file(os.path.join(tmpdir, "numpy/random/_pcg64.nuitkapython-311-darwin.a"), "numpy_random__pcg64_")
        __np__.rename_symbols_in_file(os.path.join(tmpdir, "numpy/random/_common.nuitkapython-311-darwin.a"), "numpy_random__common_")

        with WheelFile(wheel_location, 'w') as wf:
            for filename in wheel_files:
                wf.write(os.path.join(tmpdir, filename), filename)
    wheel_name = os.path.basename(wheel_location)
    shutil.copy(wheel_location, os.path.join(wheel_directory, wheel_name))
    return os.path.join(wheel_directory, wheel_name)
