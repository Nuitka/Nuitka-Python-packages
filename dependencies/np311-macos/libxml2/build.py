import __np__
import os
import sysconfig


def run(temp_dir: str):
    __np__.download_extract("https://download.gnome.org/sources/libxml2/2.9/libxml2-2.9.13.tar.xz", temp_dir)

    os.chdir(os.path.join(temp_dir, "libxml2-2.9.13"))

    __np__.run_with_output("/bin/bash",
                           "configure",
                           f"CC={sysconfig.get_config_var('CC')}",
                           f"CXX={sysconfig.get_config_var('CXX')}",
                           "--prefix=" + __np__.find_dep_root("libxml2"),
                           "--with-libiconv-prefix=" + __np__.find_dep_root("iconv"),
                           "--disable-shared")

    __np__.run_with_output("make", f"-j{__np__.get_num_jobs()}")
    __np__.run_with_output("make", "install")
