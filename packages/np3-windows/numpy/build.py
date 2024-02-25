import __np__
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
                              os.path.join(os.path.dirname(__file__), "numpy-static-patch.patch"))
    
    # In reference to https://github.com/numpy/numpy/blob/main/build_requirements.txt
    # which is NOT available in 1.24.x releases 
    __np__.run_with_output("python.exe", "-m", "pip", "install", "meson-python>=0.10.0", "--force-reinstall")
    __np__.run_with_output("python.exe", "-m", "pip", "install", "cython>=0.29.30,<3.0", "--force-reinstall")
    __np__.run_with_output("python.exe", "-m", "pip", "install", "wheel==0.38.1", "--force-reinstall")
    __np__.run_with_output("python.exe", "-m", "pip", "install", "ninja", "--force-reinstall")
    __np__.run_with_output("python.exe", "-m", "pip", "install", "spin==0.3", "--force-reinstall")
    
    __np__.run_with_output("python.exe", os.path.join(source_dir, "setup.py"), "install")    