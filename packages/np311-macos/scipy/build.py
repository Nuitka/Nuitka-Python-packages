import __np__
import glob
import shutil
import sys
import os
from tempfile import TemporaryDirectory

import setuptools.build_meta
from wheel.wheelfile import WheelFile


def run(wheel_directory):
    __np__.run_build_tool_exe("patch", "-p1", "-ui",
                              os.path.join(os.path.dirname(__file__), "scipy-static-patch.patch"))

    

    env = os.environ.copy()
    env["MACOSX_DEPLOYMENT_TARGET"] = "10.9"
    env["PEP517_BACKEND_PATH"] = os.pathsep.join([x for x in sys.path if not x.endswith(os.path.sep + "site")])
    env["PATH"] = (os.path.dirname(__np__.find_build_tool_exe("cmake", "cmake")) + os.pathsep + 
                   os.path.dirname(__np__.find_build_tool_exe("ninja", "ninja")) + os.pathsep + os.environ["PATH"])
    env["FC"] = __np__.find_build_tool_exe("clang", "flang-new")
    env["FC_LD"] = __np__.find_build_tool_exe("clang", "ld64.lld")
    env["LDFLAGS"] = "-isysroot /Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX.sdk -fuse-ld=" + __np__.find_build_tool_exe("clang", "ld64.lld")
    env["LIB"] = os.pathsep + __np__.find_dep_libs("openblas")
    env["INCLUDE"] = os.pathsep + __np__.find_dep_include("openblas")
    env["CMAKE_PREFIX_PATH"] = __np__.find_dep_root("openblas")
    __np__.run(sys.executable, "-m", "pip", "wheel", ".", "--verbose", "--no-build-isolation",
                           "-Csetup-args=-Dprefer_static=True", "-Csetup-args=-Dblas=openblas", 
                           "-Csetup-args=-Dlapack=openblas", env=env)

    wheel_location = glob.glob("scipy-*.whl")[0]

    os.environ.update(env)

    wheel_files = []
    with TemporaryDirectory() as tmpdir:
        with WheelFile(wheel_location) as wf:
            for filename in wf.namelist():
                wheel_files.append(filename)
                wf.extract(filename, tmpdir)
        __np__.rename_symbols_in_file(os.path.join(tmpdir, "scipy/optimize/_lbfgsb.nuitkapython-311-darwin.a"), "scipy_optimize__lbfgsb_")
        __np__.rename_symbols_in_file(os.path.join(tmpdir, "scipy/optimize/_slsqp.nuitkapython-311-darwin.a"), "scipy_optimize__slsqp_")
        __np__.rename_symbols_in_file(os.path.join(tmpdir, "scipy/interpolate/_dfitpack.nuitkapython-311-darwin.a"), "scipy_interpolate__dfitpack_")
        __np__.rename_symbols_in_file(os.path.join(tmpdir, "scipy/integrate/_dop.nuitkapython-311-darwin.a"), "scipy_integrate__dop_")
        __np__.rename_symbols_in_file(os.path.join(tmpdir, "scipy/integrate/_vode.nuitkapython-311-darwin.a"), "scipy_integrate__vode_")
        __np__.rename_symbols_in_file(os.path.join(tmpdir, "scipy/linalg/_fblas.nuitkapython-311-darwin.a"), "scipy_linalg__fblas_")
        __np__.rename_symbols_in_file(os.path.join(tmpdir, "scipy/stats/_mvn.nuitkapython-311-darwin.a"), "scipy_stats__mvn_")
        __np__.rename_symbols_in_file(os.path.join(tmpdir, "scipy/sparse/linalg/_propack/_cpropack.nuitkapython-311-darwin.a"), "scipy_sparse_linalg__propack__cpropack_")
        __np__.rename_symbols_in_file(os.path.join(tmpdir, "scipy/sparse/linalg/_propack/_dpropack.nuitkapython-311-darwin.a"), "scipy_sparse_linalg__propack__dpropack_")
        __np__.rename_symbols_in_file(os.path.join(tmpdir, "scipy/sparse/linalg/_propack/_spropack.nuitkapython-311-darwin.a"), "scipy_sparse_linalg__propack__spropack_")
        __np__.rename_symbols_in_file(os.path.join(tmpdir, "scipy/sparse/linalg/_propack/_zpropack.nuitkapython-311-darwin.a"), "scipy_sparse_linalg__propack__zpropack_")
        with WheelFile(wheel_location, 'w') as wf:
            for filename in wheel_files:
                wf.write(os.path.join(tmpdir, filename), filename)

    wheel_name = os.path.basename(wheel_location)
    shutil.copy(wheel_location, os.path.join(wheel_directory, wheel_name))
    return os.path.join(wheel_directory, wheel_name)
