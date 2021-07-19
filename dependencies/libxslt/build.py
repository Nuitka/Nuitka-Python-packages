import nputils
import shutil
import os


def run(temp_dir: str):
    nputils.download_extract("https://github.com/GNOME/libxslt/archive/refs/tags/v1.1.34.zip", temp_dir)

    os.chdir(os.path.join(temp_dir, "libxslt-1.1.34", "win32"))

    nputils.run_build_tool_exe("patch", "patch.exe", "--binary", "configure.js", os.path.join(temp_dir, "configure.js.patch"))

    nputils.run_compiler_exe(
        "cscript.exe", "configure.js",
        "compiler=msvc",
        "prefix=" + os.path.join(temp_dir, "install_tmp"),
        "cruntime=/MT",
        "include=" + nputils.find_dep_include("iconv") + ";" + nputils.find_dep_include("libxml2"),
        "lib=" + nputils.find_dep_libs("iconv") + ";" + nputils.find_dep_libs("libxml2"))

    nputils.setup_compiler_env()

    nputils.nmake("/f", "Makefile.msvc", "LIBS=iconv.lib Ws2_32.lib")
    nputils.nmake("/f", "Makefile.msvc", "install")

    shutil.copy(os.path.join(temp_dir, "install_tmp", "lib", "libxslt_a.lib"), os.path.join(temp_dir, "libxslt.lib"))
    shutil.copy(os.path.join(temp_dir, "install_tmp", "lib", "libxslt_a.lib"), os.path.join(temp_dir, "libxslt_a.lib"))
    shutil.copy(os.path.join(temp_dir, "install_tmp", "lib", "libexslt_a.lib"), os.path.join(temp_dir, "libexslt.lib"))
    shutil.copy(os.path.join(temp_dir, "install_tmp", "lib", "libexslt_a.lib"), os.path.join(temp_dir, "libexslt_a.lib"))

    nputils.prepend_to_file(os.path.join(temp_dir, "install_tmp", "include", "libxslt", "xsltexports.h"), "#define LIBXSLT_STATIC\n")
    nputils.prepend_to_file(os.path.join(temp_dir, "install_tmp", "include", "libexslt", "exsltexports.h"), "#define LIBEXSLT_STATIC\n")

    nputils.install_dep_libs("libxslt", os.path.join(temp_dir, "*.lib"))
    nputils.install_dep_include("libxslt", os.path.join(temp_dir, "install_tmp", "include", "*"))
