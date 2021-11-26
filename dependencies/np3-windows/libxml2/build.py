import nputils
import shutil
import os


def run(temp_dir: str):
    nputils.download_extract("https://github.com/GNOME/libxml2/archive/refs/tags/v2.9.12.zip", temp_dir)

    os.chdir(os.path.join(temp_dir, "libxml2-2.9.12", "win32"))

    nputils.run_compiler_exe(
        "cscript.exe", "configure.js",
        "compiler=msvc",
        "prefix=" + os.path.join(temp_dir, "install_tmp"),
        "cruntime=/MT",
        "include=" + nputils.find_dep_include("iconv"),
        "lib=" + nputils.find_dep_libs("iconv"))

    nputils.setup_compiler_env()

    nputils.nmake("/f", "Makefile.msvc")
    nputils.nmake("/f", "Makefile.msvc", "install")

    shutil.copy(os.path.join(temp_dir, "install_tmp", "lib", "libxml2_a.lib"), os.path.join(temp_dir, "libxml2.lib"))
    shutil.copy(os.path.join(temp_dir, "install_tmp", "lib", "libxml2_a.lib"), os.path.join(temp_dir, "libxml2_a.lib"))

    nputils.prepend_to_file(os.path.join(temp_dir, "install_tmp", "include", "libxml2", "libxml", "xmlexports.h"), "#define LIBXML_STATIC\n")

    nputils.install_dep_libs("libxml2", os.path.join(temp_dir, "libxml2.lib"), os.path.join(temp_dir, "libxml2_a.lib"))
    nputils.install_dep_include("libxml2", os.path.join(temp_dir, "install_tmp", "include", "libxml2", "*"))
