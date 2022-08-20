import __np__
import glob
import shutil
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

    __np__.setup_compiler_env()

    os.chdir(source_dir)

    __np__.run_build_tool_exe("patch", "patch.exe", "--binary", "-p1", "-i",
                              os.path.join(os.path.dirname(__file__), "Implement_static_python_build.patch"))

    os.makedirs(os.path.join("thirdparty", "win-libs-vc14-x64"), exist_ok=True)

    shutil.copytree(__np__.find_dep_root("bullet"), os.path.join("thirdparty", "win-libs-vc14-x64", "bullet"))
    shutil.copytree(__np__.find_dep_root("eigen"), os.path.join("thirdparty", "win-libs-vc14-x64", "eigen"))
    shutil.copytree(__np__.find_dep_root("freetype"), os.path.join("thirdparty", "win-libs-vc14-x64", "freetype"))
    shutil.copytree(__np__.find_dep_include("freetype"), os.path.join("thirdparty", "win-libs-vc14-x64", "freetype", "include", "freetype2"))
    shutil.copytree(__np__.find_dep_root("harfbuzz"), os.path.join("thirdparty", "win-libs-vc14-x64", "harfbuzz"))
    shutil.copytree(__np__.find_dep_root("jpeg"), os.path.join("thirdparty", "win-libs-vc14-x64", "jpeg"))
    shutil.copytree(__np__.find_dep_root("nvidiacg"), os.path.join("thirdparty", "win-libs-vc14-x64", "nvidiacg"))
    shutil.copytree(__np__.find_dep_root("ode"), os.path.join("thirdparty", "win-libs-vc14-x64", "ode"))
    shutil.copytree(__np__.find_dep_root("ogg"), os.path.join("thirdparty", "win-libs-vc14-x64", "ogg"))
    shutil.copytree(__np__.find_dep_root("openal"), os.path.join("thirdparty", "win-libs-vc14-x64", "openal"))
    shutil.copytree(__np__.find_dep_root("openssl"), os.path.join("thirdparty", "win-libs-vc14-x64", "openssl"))
    shutil.copytree(__np__.find_dep_root("opusfile"), os.path.join("thirdparty", "win-libs-vc14-x64", "opusfile"))
    __np__.install_files(os.path.join("thirdparty", "win-libs-vc14-x64", "opus", "lib"),
                         os.path.join(__np__.find_dep_libs("opus"), "*.lib"),
                         os.path.join(__np__.find_dep_libs("opusfile"), "*.lib"),
                         os.path.join(__np__.find_dep_libs("ogg"), "*.lib"))
    __np__.install_files(os.path.join("thirdparty", "win-libs-vc14-x64", "opus", "include", "opus"),
                         os.path.join(__np__.find_dep_include("opus"), "*.h"),
                         os.path.join(__np__.find_dep_include("opusfile"), "*.h"))
    __np__.install_files(os.path.join("thirdparty", "win-libs-vc14-x64", "opus", "include", "ogg"),
                         os.path.join(__np__.find_dep_include("ogg"), "ogg", "*.h"))
    shutil.copytree(__np__.find_dep_root("png"), os.path.join("thirdparty", "win-libs-vc14-x64", "png"))
    shutil.copytree(__np__.find_dep_root("squish"), os.path.join("thirdparty", "win-libs-vc14-x64", "squish"))
    shutil.copytree(__np__.find_dep_root("tiff"), os.path.join("thirdparty", "win-libs-vc14-x64", "tiff"))
    __np__.install_files(os.path.join("thirdparty", "win-libs-vc14-x64", "vorbis", "lib"),
                         os.path.join(__np__.find_dep_libs("vorbis"), "*.lib"),
                         os.path.join(__np__.find_dep_libs("ogg"), "*.lib"))
    shutil.copytree(__np__.find_dep_include("vorbis"), os.path.join("thirdparty", "win-libs-vc14-x64", "vorbis", "include"))
    __np__.install_files(os.path.join("thirdparty", "win-libs-vc14-x64", "vorbis", "include", "ogg"),
                         os.path.join(__np__.find_dep_include("ogg"), "ogg", "*.h"))
    shutil.copytree(__np__.find_dep_root("zlib"), os.path.join("thirdparty", "win-libs-vc14-x64", "zlib"))

    __np__.run_with_output("python.exe", os.path.join(source_dir, "makepanda", "makepanda.py"), "--everything", "--wheel", "--static", "--msvc-version=14.2", "--windows-sdk=10", "--threads=8", "--optimize=4")
    __np__.run_with_output("python.exe", "-m", "pip", "install", glob.glob("panda3d*.whl")[0], "--force-reinstall")
