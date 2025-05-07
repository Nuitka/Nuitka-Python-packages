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

    __np__.run_build_tool_exe("patch", "patch.exe", "-t", "-p1", "-i",
                              os.path.join(os.path.dirname(__file__), "pandas-static-patch.patch"))

    __np__.run(sys.executable, "-m", "build", "-w", "--no-isolation")

    wheel_location = glob.glob(os.path.join("dist", "pandas-*.whl"))[0]

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
        __np__.rename_symbols_in_file(os.path.join(tmpdir, "pandas\\_libs\\interval.lib"), "pandas__libs_interval")
        __np__.rename_symbols_in_file(os.path.join(tmpdir, "pandas\\_libs\\parsers.lib"), "pandas__libs_parsers")
        __np__.rename_symbols_in_file(os.path.join(tmpdir, "pandas\\_libs\\algos.lib"), "pandas__libs_algos")
        __np__.rename_symbols_in_file(os.path.join(tmpdir, "pandas\\_libs\\hashtable.lib"), "pandas__libs_hashtable")
        __np__.rename_symbols_in_file(os.path.join(tmpdir, "pandas\\_libs\\join.lib"), "pandas__libs_join")
        __np__.rename_symbols_in_file(os.path.join(tmpdir, "pandas\\_libs\\index.lib"), "pandas__libs_index")
        __np__.rename_symbols_in_file(os.path.join(tmpdir, "pandas\\_libs\\pandas_datetime.lib"), "pandas__libs_pandas_datetime")
        __np__.rename_symbols_in_file(os.path.join(tmpdir, "pandas\\_libs\\json.lib"), "pandas__libs_json")
        with WheelFile(wheel_location, 'w') as wf:
            for filename in wheel_files:
                wf.write(os.path.join(tmpdir, filename), filename)

    wheel_name = os.path.basename(wheel_location)
    shutil.copy(wheel_location, os.path.join(wheel_directory, wheel_name))
    return os.path.join(wheel_directory, wheel_name)
