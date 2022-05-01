import __np__
from typing import *

import os
import shutil
import sysconfig


def run(temp_dir: str):
    __np__.download_extract("https://ftp.gnu.org/pub/gnu/libiconv/libiconv-1.16.tar.gz", temp_dir)

    os.chdir(os.path.join(temp_dir, "libiconv-1.16"))

    __np__.run_with_output("/bin/bash",
                           "configure",
                           f"CC={sysconfig.get_config_var('CC')}",
                           f"CXX={sysconfig.get_config_var('CXX')}",
                           "--prefix=" + __np__.find_dep_root("iconv"),
                           "--disable-shared")

    __np__.run_with_output("make", f"-j{__np__.get_num_jobs()}")
    __np__.run_with_output("make", "install")
