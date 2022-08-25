import __np__
import glob
import shutil
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
                              os.path.join(os.path.dirname(__file__), "Implement_static_build.patch"))

    os.makedirs(os.path.join("thirdparty", "linux-libs-x64"), exist_ok=True)

    shutil.copytree(__np__.find_dep_root("bullet"), os.path.join("thirdparty", "linux-libs-x64", "bullet"))
    shutil.copytree(__np__.find_dep_root("eigen"), os.path.join("thirdparty", "linux-libs-x64", "eigen"))
    shutil.copytree(__np__.find_dep_root("freetype"), os.path.join("thirdparty", "linux-libs-x64", "freetype"))
    shutil.copytree(__np__.find_dep_include("freetype"), os.path.join("thirdparty", "linux-libs-x64", "freetype", "include", "freetype2"))
    shutil.copytree(__np__.find_dep_root("harfbuzz"), os.path.join("thirdparty", "linux-libs-x64", "harfbuzz"))
    shutil.copytree(__np__.find_dep_root("jpeg"), os.path.join("thirdparty", "linux-libs-x64", "jpeg"))
    shutil.copytree(__np__.find_dep_root("nvidiacg"), os.path.join("thirdparty", "linux-libs-x64", "nvidiacg"))
    shutil.copytree(__np__.find_dep_root("ode"), os.path.join("thirdparty", "linux-libs-x64", "ode"))
    shutil.copytree(__np__.find_dep_root("ogg"), os.path.join("thirdparty", "linux-libs-x64", "ogg"))
    shutil.copytree(__np__.find_dep_root("openal"), os.path.join("thirdparty", "linux-libs-x64", "openal"))
    shutil.copytree(__np__.find_dep_root("openssl"), os.path.join("thirdparty", "linux-libs-x64", "openssl"))
    shutil.copytree(__np__.find_dep_root("opusfile"), os.path.join("thirdparty", "linux-libs-x64", "opusfile"))
    __np__.install_files(os.path.join("thirdparty", "linux-libs-x64", "opus", "lib"),
                         os.path.join(__np__.find_dep_libs("opus"), "*.a"),
                         os.path.join(__np__.find_dep_libs("opusfile"), "*.a"),
                         os.path.join(__np__.find_dep_libs("ogg"), "*.a"))
    __np__.install_files(os.path.join("thirdparty", "linux-libs-x64", "opus", "include", "opus"),
                         os.path.join(__np__.find_dep_include("opus"), "*.h"),
                         os.path.join(__np__.find_dep_include("opusfile"), "*.h"))
    __np__.install_files(os.path.join("thirdparty", "linux-libs-x64", "opus", "include", "ogg"),
                         os.path.join(__np__.find_dep_include("ogg"), "ogg", "*.h"))
    shutil.copytree(__np__.find_dep_root("png"), os.path.join("thirdparty", "linux-libs-x64", "png"))
    shutil.copytree(__np__.find_dep_root("squish"), os.path.join("thirdparty", "linux-libs-x64", "squish"))
    shutil.copytree(__np__.find_dep_root("tiff"), os.path.join("thirdparty", "linux-libs-x64", "tiff"))
    __np__.install_files(os.path.join("thirdparty", "linux-libs-x64", "vorbis", "lib"),
                         os.path.join(__np__.find_dep_libs("vorbis"), "*.a"),
                         os.path.join(__np__.find_dep_libs("ogg"), "*.a"))
    shutil.copytree(__np__.find_dep_include("vorbis"), os.path.join("thirdparty", "linux-libs-x64", "vorbis", "include"))
    __np__.install_files(os.path.join("thirdparty", "linux-libs-x64", "vorbis", "include", "ogg"),
                         os.path.join(__np__.find_dep_include("ogg"), "ogg", "*.h"))
    shutil.copytree(__np__.find_dep_root("zlib"), os.path.join("thirdparty", "linux-libs-x64", "zlib"))

    __np__.run_with_output(sys.executable, os.path.join(source_dir, "makepanda", "makepanda.py"), "--everything", "--wheel", "--static", "--threads=8", "--optimize=4")
    __np__.run_with_output(sys.executable, "-m", "pip", "install", glob.glob("panda3d*.whl")[0], "--force-reinstall")
