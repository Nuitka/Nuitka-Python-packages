import __np__
import glob
import shutil
import sys
import os
import setuptools.build_meta
from tempfile import TemporaryDirectory

from wheel.wheelfile import WheelFile


def run(wheel_directory):
    __np__.setup_compiler_env()

    with TemporaryDirectory() as temp_dir:
        __np__.run(sys.executable, "-m", "build", "-w", "--no-isolation", "-Ccompile-args=-j3", "-Cbuild-dir=" + temp_dir)

    wheel_location = glob.glob(os.path.join("dist", "scikit_learn-*.whl"))[0]

    env = os.environ.copy()
    env["PATH"] = (os.path.dirname(__np__.find_build_tool_exe("7zip", "7z.exe")) + os.path.pathsep +
                   os.path.dirname(__np__.find_build_tool_exe("mingw", "objdump.exe")) + os.path.pathsep + env["PATH"])
    os.environ.update(env)
    wheel_files = []
    with TemporaryDirectory() as tmpdir:
        with WheelFile(wheel_location) as wf:
            for filename in wf.namelist():
                wheel_files.append(filename)
                wf.extract(filename, tmpdir)
        __np__.rename_symbols_in_file(os.path.join(tmpdir, "sklearn\\svm\\_libsvm_sparse.lib"), "sklearn_svm__libsvm_sparse_")
        __np__.rename_symbols_in_file(os.path.join(tmpdir, "sklearn\\svm\\_libsvm.lib"), "sklearn_svm__libsvm_")
        __np__.rename_symbols_in_file(os.path.join(tmpdir, "sklearn\\svm\\_newrand.lib"), "sklearn_svm__newrand_")
        __np__.rename_symbols_in_file(os.path.join(tmpdir, "sklearn\\svm\\_liblinear.lib"), "sklearn_svm__liblinear_")
        with WheelFile(wheel_location, 'w') as wf:
            for filename in wheel_files:
                wf.write(os.path.join(tmpdir, filename), filename)

    wheel_name = os.path.basename(wheel_location)
    shutil.copy(wheel_location, os.path.join(wheel_directory, wheel_name))
    return os.path.join(wheel_directory, wheel_name)
