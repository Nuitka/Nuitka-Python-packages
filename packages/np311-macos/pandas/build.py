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

    wheel_location = glob.glob(os.path.join("dist", "pandas-*.whl"))[0]

    wheel_files = []
    with TemporaryDirectory() as tmpdir:
        with WheelFile(wheel_location) as wf:
            for filename in wf.namelist():
                wheel_files.append(filename)
                wf.extract(filename, tmpdir)
        __np__.rename_symbols_in_file(os.path.join(tmpdir, "pandas/_libs/lib.nuitkapython-311-darwin.a"), "pandas__libs_lib")
        __np__.rename_symbols_in_file(os.path.join(tmpdir, "pandas/_libs/interval.nuitkapython-311-darwin.a"), "pandas__libs_interval")
        __np__.rename_symbols_in_file(os.path.join(tmpdir, "pandas/_libs/parsers.nuitkapython-311-darwin.a"), "pandas__libs_parsers")
        __np__.rename_symbols_in_file(os.path.join(tmpdir, "pandas/_libs/algos.nuitkapython-311-darwin.a"), "pandas__libs_algos")
        __np__.rename_symbols_in_file(os.path.join(tmpdir, "pandas/_libs/hashtable.nuitkapython-311-darwin.a"), "pandas__libs_hashtable")
        __np__.rename_symbols_in_file(os.path.join(tmpdir, "pandas/_libs/join.nuitkapython-311-darwin.a"), "pandas__libs_join")
        __np__.rename_symbols_in_file(os.path.join(tmpdir, "pandas/_libs/index.nuitkapython-311-darwin.a"), "pandas__libs_index")
        __np__.rename_symbols_in_file(os.path.join(tmpdir, "pandas/_libs/pandas_datetime.nuitkapython-311-darwin.a"), "pandas__libs_pandas_datetime")
        __np__.rename_symbols_in_file(os.path.join(tmpdir, "pandas/_libs/json.nuitkapython-311-darwin.a"), "pandas__libs_json")
        with WheelFile(wheel_location, 'w') as wf:
            for filename in wheel_files:
                wf.write(os.path.join(tmpdir, filename), filename)

    wheel_name = os.path.basename(wheel_location)
    shutil.copy(wheel_location, os.path.join(wheel_directory, wheel_name))
    return os.path.join(wheel_directory, wheel_name)
