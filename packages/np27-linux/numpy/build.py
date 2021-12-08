import __np__

import sys, os


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

    __np__.my_print("Starting numpy patching...")
    __np__.apply_patch(os.path.join(temp_dir, "numpy-static-patch.patch"), ".")

    __np__.my_print("Starting numpy compilation...")
    __np__.run_with_output(sys.executable, os.path.join(source_dir, "setup.py"), "install")
