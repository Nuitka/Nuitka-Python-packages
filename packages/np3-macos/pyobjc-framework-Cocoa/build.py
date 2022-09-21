import __np__
import sys
from typing import *
from pip._internal.req.req_install import InstallRequirement

import os


def run(req: InstallRequirement,
        temp_dir: str,
        source_dir: str,
        install_options: List[str],
        global_options: Optional[Sequence[str]],
        root: Optional[str],
        home: Optional[str],
        prefix: Optional[str],
        warn_script_location: bool,
        use_user_site: bool,
        pycompile: bool
        ):

    os.chdir(source_dir)

    __np__.run_with_output("patch", "--binary", "-p1", "-i",
                              os.path.join(os.path.dirname(__file__), "Disable-test.patch"))

    os.environ["MACOSX_DEPLOYMENT_TARGET"] = "10.9"

    __np__.run_with_output(sys.executable, os.path.join(source_dir, "setup.py"), "install")

