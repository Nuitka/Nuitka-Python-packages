import __np__
import json
import shutil
import os
import sysconfig


def run(temp_dir: str):
    __np__.download_extract("https://download.gnome.org/sources/libxslt/1.1/libxslt-1.1.35.tar.xz", temp_dir)

    os.chdir(os.path.join(temp_dir, "libxslt-1.1.35"))

    __np__.run_with_output("/bin/bash",
                           "configure",
                           f"CC={sysconfig.get_config_var('CC')}",
                           f"CXX={sysconfig.get_config_var('CXX')}",
                           "--prefix=" + __np__.find_dep_root("libxslt"),
                           "--with-libxml-prefix=" + __np__.find_dep_root("libxml2"),
                           "--disable-shared")

    __np__.run_with_output("make", f"-j{__np__.get_num_jobs()}")
    __np__.run_with_output("make", "install")

    with open(os.path.join(__np__.find_dep_libs("libxslt"), "libexslt.a.link.json"), 'w') as f:
        json.dump({'libraries': ['gcrypt'], "library_dirs": []}, f)
