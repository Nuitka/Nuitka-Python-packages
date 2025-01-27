import __np__
import glob
import shutil
import sys
import os
import setuptools.build_meta


def run(wheel_directory):
    __np__.run("patch", "-t", "-p1", "-i",
                              os.path.join(os.path.dirname(__file__), "meson-static-patch.patch"))

    os.environ["PEP517_BACKEND_PATH"] = os.pathsep.join([x for x in sys.path if not x.endswith(os.path.sep + "site")])
    __np__.run_with_output(sys.executable, "-m", "pip", "wheel", ".", "--verbose")

    wheel_location = glob.glob("meson-*.whl")[0]
    wheel_name = os.path.basename(wheel_location)
    shutil.copy(wheel_location, os.path.join(wheel_directory, wheel_name))
    return os.path.join(wheel_directory, wheel_name)
