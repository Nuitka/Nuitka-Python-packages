import __np__
import glob
import shutil
import sys
import os
import platform
import setuptools.build_meta


def run(wheel_directory):
    os.environ["MACOSX_DEPLOYMENT_TARGET"] = "10.9"

    shutil.copyfile(os.path.join(os.path.dirname(__file__), "core.py"), "certifi/core.py")
    os.remove("certifi/cacert.pem")

    __np__.run_with_output(sys.executable, "setup.py", "bdist_wheel")

    wheel_location = glob.glob(os.path.join("dist", "certifi-*.whl"))[0]
    wheel_name = os.path.basename(wheel_location)
    shutil.copy(wheel_location, os.path.join(wheel_directory, wheel_name))
    return os.path.join(wheel_directory, wheel_name)
