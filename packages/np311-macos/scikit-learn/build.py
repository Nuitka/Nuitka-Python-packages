import __np__
import glob
import shutil
import sys
import os
import sysconfig
import setuptools.build_meta
from tempfile import TemporaryDirectory
from wheel.wheelfile import WheelFile


def run(wheel_directory):
    env = os.environ.copy()
    env["MACOSX_DEPLOYMENT_TARGET"] = "10.9"
    env["PEP517_BACKEND_PATH"] = os.pathsep.join([x for x in sys.path if not x.endswith(os.path.sep + "site")])
    env["PATH"] = (os.path.dirname(__np__.find_build_tool_exe("cmake", "cmake")) + os.pathsep +
                   os.path.dirname(__np__.find_build_tool_exe("ninja", "ninja")) + os.pathsep + os.environ["PATH"])
    env["PKG_CONFIG"] = "/disabled"
    __np__.run(sys.executable, "-m", "build", "-w", "--no-isolation", env=env)

    wheel_location = glob.glob(os.path.join("dist", "scikit_learn-*.whl"))[0]

    wheel_files = []
    with TemporaryDirectory() as tmpdir:
        with WheelFile(wheel_location) as wf:
            for filename in wf.namelist():
                wheel_files.append(filename)
                wf.extract(filename, tmpdir)
        __np__.rename_symbols_in_file(os.path.join(tmpdir, "sklearn/svm/_libsvm_sparse.nuitkapython-311-darwin.a"), "sklearn_svm__libsvm_sparse")
        __np__.rename_symbols_in_file(os.path.join(tmpdir, "sklearn/svm/_libsvm.nuitkapython-311-darwin.a"), "sklearn_svm__libsvm")
        __np__.rename_symbols_in_file(os.path.join(tmpdir, "sklearn/svm/_newrand.nuitkapython-311-darwin.a"), "sklearn_svm__newrand")
        __np__.rename_symbols_in_file(os.path.join(tmpdir, "sklearn/svm/_liblinear.nuitkapython-311-darwin.a"), "sklearn_svm__liblinear")
        __np__.remove_symbols_in_file(os.path.join(tmpdir, "scikit-learn/libliblinear-skl.a"), "src_liblinear_linear.cpp.o", ["_set_seed", "set_seed", "_mt_rand", "mt_rand"])
        with WheelFile(wheel_location, 'w') as wf:
            for filename in wheel_files:
                wf.write(os.path.join(tmpdir, filename), filename)

    wheel_name = os.path.basename(wheel_location)
    shutil.copy(wheel_location, os.path.join(wheel_directory, wheel_name))
    return os.path.join(wheel_directory, wheel_name)
