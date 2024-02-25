import __np__
from typing import *
from pip._internal.req.req_install import InstallRequirement
import os
from pathlib import Path

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
                              os.path.join(os.path.dirname(__file__), "cffi-static-patch.patch"))
    
    # ctypes already include ffi library
    libffi_path = os.path.join(source_dir, "c", "libffi_x86_x64")
    for p in Path(libffi_path).glob("*.c"):
        p.unlink()
    
    __np__.run_with_output("python.exe", "-m", "pip", "install", "pycparser", "--force-reinstall")
    __np__.run_with_output("python.exe", "-m", "pip", "install", "pytest", "--force-reinstall")
   
    __np__.run_with_output("python.exe", os.path.join(source_dir, "setup.py"), "install")    