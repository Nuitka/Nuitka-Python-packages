import __np__
import glob
import shutil
import sys
import os
import setuptools.build_meta


def run(wheel_directory):
    __np__.run("patch", "-t", "-p1", "-i",
                              os.path.join(os.path.dirname(__file__), "pip-static-patch.patch"))

    __np__.run_with_output(sys.executable, "-m", "build", "-w", "--no-isolation")

    wheel_location = glob.glob(os.path.join("dist", "pip-*.whl"))[0]
    wheel_name = os.path.basename(wheel_location)
    shutil.copy(wheel_location, os.path.join(wheel_directory, wheel_name))
    return os.path.join(wheel_directory, wheel_name)
