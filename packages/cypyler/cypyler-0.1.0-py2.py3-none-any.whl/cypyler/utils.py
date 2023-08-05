import importlib

from distutils.core import Distribution, Extension
from distutils.command.build_ext import build_ext

from Cython.Build import cythonize


def _get_build_extension(extension, lib_dir):
    dist = Distribution()
    config_files = dist.find_config_files()

    # TODO: Is this check really useful?
    try:
        config_files.remove('setup.cfg')
    except ValueError:
        pass

    dist.parse_config_files(config_files)

    build_extension_ = build_ext(dist)
    build_extension_.finalize_options()

    build_extension_.build_temp = lib_dir
    build_extension_.build_lib = lib_dir
    build_extension_.extensions = [extension]

    return build_extension_


def build_extension(extension, lib_dir):
    build_extension_ = _get_build_extension(
        extension, lib_dir=lib_dir)
    build_extension_.run()

    return build_extension_


def cypyle(modname, pyxfilename, libraries=None, include_dirs=None):
    if not libraries:
        libraries = []
    if not include_dirs:
        include_dirs = []

    import numpy as np
    ext = Extension(name=modname,
                    sources=[pyxfilename],
                    include_dirs=[np.get_include()]+include_dirs,
                    language="c++",
                    libraries=libraries)

    opts = dict(
        force=True
    )

    return cythonize([ext], **opts)


def import_extension(module_name, ext_path):
    spec = importlib.util.spec_from_file_location(module_name, ext_path)
    mod = importlib.util.module_from_spec(spec)

    return mod
