import __np__
import glob
import sys
from typing import *
from pip._internal.req.req_install import InstallRequirement

import os


def run(temp_dir: str, source_dir: str,):

    os.chdir(source_dir)

    os.environ["LXML_STATIC_INCLUDE_DIRS"] = os.pathsep.join([
        __np__.find_dep_include("iconv"),
        os.path.join(__np__.find_dep_include("xml2"), "libxml2"),
        __np__.find_dep_include("xslt")
    ])

    os.environ["LXML_STATIC_LIBRARY_DIRS"] = os.pathsep.join([
        __np__.find_dep_libs("iconv"),
        __np__.find_dep_libs("xml2"),
        __np__.find_dep_libs("xslt")
    ])

    __np__.run_with_output(sys.executable, os.path.join(source_dir, "setup.py"), "--static", "bdist_wheel")

    return glob.glob(os.path.join(source_dir, "dist", "*.whl"))[0]
