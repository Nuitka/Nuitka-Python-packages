import __np__

from pip._internal.req.req_install import InstallRequirement

import os


def run(req,
        temp_dir,
        source_dir,
        install_options,
        global_options,
        root,
        home,
        prefix,
        warn_script_location,
        use_user_site,
        pycompilel
        ):

    __np__.setup_compiler_env()

    os.chdir(source_dir)

    __np__.run_build_tool_exe("patch", "patch", "numpy-static-patch.patch")

    __np__.run_with_output("python", os.path.join(source_dir, "setup.py"), "install")
