import nputils
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

    nputils.setup_compiler_env()

    os.chdir(source_dir)

    nputils.run_build_tool_exe("patch", "patch.exe", "--binary", "setup.py", os.path.join(temp_dir, "c9cf865d2e5f4ea4952d0ea6d4e0e2e2120649b7.patch"))

    os.environ["LXML_STATIC_INCLUDE_DIRS"] = os.pathsep.join([
        nputils.find_dep_include("iconv"),
        nputils.find_dep_include("libxml2"),
        nputils.find_dep_include("libxslt")
    ])

    os.environ["LXML_STATIC_LIBRARY_DIRS"] = os.pathsep.join([
        nputils.find_dep_libs("iconv"),
        nputils.find_dep_libs("libxml2"),
        nputils.find_dep_libs("libxslt"),
        nputils.find_dep_libs("zlib")
    ])

    nputils.run_with_output("python.exe", os.path.join(source_dir, "setup.py"), "--static", "install")
