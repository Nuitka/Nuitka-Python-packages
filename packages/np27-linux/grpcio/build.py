import __np__



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
        pycompile
        ):

    __np__.auto_patch_Cython_memcpy(source_dir)

    # Let standard procedure run too.
    return True

