import glob
import os
import sysconfig


def run(temp_dir: str, source_dir: str,):
    return glob.glob(os.path.join(sysconfig.get_config_var("LIBDEST"), "ensurepip", "_bundled", "setuptools*.whl"))[0]
