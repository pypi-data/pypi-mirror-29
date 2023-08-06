#!/usr/bin/env python

import os
import sys
import glob
import platform
import numpy as np
import unittest
from setuptools import setup, Extension

try:
    import pybind11
except ImportError:
    import pip
    pip.main(['install', 'pybind11'])
    import pybind11

# ======= S E T T I N G S ======= #
femzip_path_windows = "libs/femzip/FEMZIP_8.68_dyna_NO_OMP_Windows_VS2012_MD_x64/x64"  # optional
femzip_path_linux = "libs/femzip/Linux64/64Bit/"  # optional
# ====== D E V E L O P E R ====== #
debugging_mode = False
measure_time = False
use_openmp = True
version = "0.7.1"
# =============================== #
is_windows = (platform.system() == "Windows")
is_linux = (platform.system() in ["Linux", "Darwin"])
# =============================== #


def setup_dyna_cpp():

    include_dirs = ["qd/cae",
                    np.get_include(),
                    pybind11.get_include()]
    srcs = [
        "qd/cae/dyna_cpp/python_api/pybind_wrapper.cpp",
        "qd/cae/dyna_cpp/db/FEMFile.cpp",
        "qd/cae/dyna_cpp/db/DB_Elements.cpp",
        "qd/cae/dyna_cpp/db/DB_Nodes.cpp",
        "qd/cae/dyna_cpp/db/DB_Parts.cpp",
        "qd/cae/dyna_cpp/db/Element.cpp",
        "qd/cae/dyna_cpp/db/Node.cpp",
        "qd/cae/dyna_cpp/db/Part.cpp",
        "qd/cae/dyna_cpp/dyna/D3plotBuffer.cpp",
        "qd/cae/dyna_cpp/dyna/D3plot.cpp",
        "qd/cae/dyna_cpp/dyna/RawD3plot.cpp",
        "qd/cae/dyna_cpp/dyna/KeyFile.cpp",
        "qd/cae/dyna_cpp/dyna/Keyword.cpp",
        "qd/cae/dyna_cpp/dyna/NodeKeyword.cpp",
        "qd/cae/dyna_cpp/dyna/ElementKeyword.cpp",
        "qd/cae/dyna_cpp/dyna/PartKeyword.cpp",
        "qd/cae/dyna_cpp/dyna/IncludeKeyword.cpp",
        "qd/cae/dyna_cpp/dyna/IncludePathKeyword.cpp",
        "qd/cae/dyna_cpp/utility/FileUtility.cpp",
        "qd/cae/dyna_cpp/utility/TextUtility.cpp"]

    # linux compiler args
    if is_linux:
        compiler_args = ["-std=c++14",
                         "-O3",
                         "-fPIC",
                         "-DQD_VERSION=\"" + version + "\""]

        if debugging_mode:
            compiler_args.append("-DQD_DEBUG")
        if measure_time:
            compiler_args.append("-DQD_MEASURE_TIME")

    # windowscompiler args
    elif is_windows:
        compiler_args = ["/EHa",
                         "/DQD_VERSION=\\\"" + version + "\\\""]
        if debugging_mode:
            compiler_args.append("/DQD_DEBUG")
        if measure_time:
            compiler_args.append("/DQD_MEASURE_TIME")
        if use_openmp:
            compiler_args.append("/openmp")

    else:
        raise RuntimeError("Could not determine os (windows or linux)")

    return srcs, include_dirs, compiler_args


def setup_dyna_cpp_binout(srcs, compiler_args):

    srcs = ["qd/cae/dyna_cpp/dyna/Binout.cpp",
            "qd/cae/dyna_cpp/dyna/lsda/lsda.c",
            "qd/cae/dyna_cpp/dyna/lsda/btree.c",
            "qd/cae/dyna_cpp/dyna/lsda/lsdatable.c",
            "qd/cae/dyna_cpp/dyna/lsda/lsdatypes.c",
            "qd/cae/dyna_cpp/dyna/lsda/trans.c",
            "qd/cae/dyna_cpp/dyna/lsda/lsdaf2c.c"] + srcs

    if is_linux:
        compiler_args += ["-fpermissive"]

    return srcs, compiler_args


def setup_dyna_cpp_femzip(srcs, lib_dirs, libs, compiler_args):
    ''' Checks for femzip libraries
    '''

    # Uses FEMZIP, iff link librares are present
    # You need to download the femzip libraries yourself from SIDACT GmbH
    # www.sidact.de
    # If you have questions, write a mail.

    # windows
    if is_windows and os.path.isdir(os.path.join(femzip_path_windows)):

        srcs.append("qd/cae/dyna_cpp/dyna/FemzipBuffer.cpp")
        lib_dirs.append(os.path.join(femzip_path_windows))
        libs += ['femunziplib_standard_dyna', 'ipp_zlibd', 'ippcoremt',
                 'ippdcmt', 'ippsmt', 'ifwin', 'ifconsol', 'ippvmmt', 'libmmd',
                 'libirc', 'svml_dispmd', 'msvcrt']
        compiler_args.append("/DQD_USE_FEMZIP")

    # linux
    elif is_linux and os.path.isdir(femzip_path_linux):

        srcs.append("qd/cae/dyna_cpp/dyna/FemzipBuffer.cpp")
        lib_dirs.append(femzip_path_linux)
        libs += ['femunzip_dyna_standard', 'ipp_z', 'ippcore',
                 'ippdc', 'ipps', 'ifcore_pic', 'ifcoremt', 'imf',
                 'ipgo', 'irc', 'svml', 'ippcore_l', 'stdc++', 'dl']
        compiler_args.append("-DQD_USE_FEMZIP")
    else:
        print("FEMZIP library not found. Compiling without FEMZIP.")

    return srcs, lib_dirs, libs, compiler_args


def setup_dyna_cpp_hdf5(srcs, compiler_args, libs, lib_dirs, include_dirs):
    ''' Sets up the hdf5 compilation
    '''

    srcs.append("qd/cae/dyna_cpp/utility/HDF5_Utility.cpp")

    if is_linux:
        compiler_args.append("-DQD_USE_HDF5")
        raise RuntimeError("Linux HDF5 compilation missing.")

    if is_windows:

        import ntpath
        files = glob.glob("libs/hdf5/windows/lib/lib*.lib")
        files = [ntpath.basename(entry).replace(".lib", "") for entry in files]
        libs += files

        lib_dirs.append("libs/hdf5/windows/lib")
        include_dirs.append("libs/hdf5/windows/include")
        compiler_args.append("/DQD_USE_HDF5")

    return srcs, compiler_args, libs, lib_dirs, include_dirs


def use_vtk_if_possible(depency_packages):

    # do nothing if missing
    if not os.path.isdir('./libs/VTK'):
        return []

    # packages
    depency_packages = ['autobahn', 'constantly', 'hyperlink',
                        'incremental', 'Twisted', 'txaio', 'wslink', 'zope.interface']

    ''' put in top of init
    import os
    import sys

    # add runtime libraries to environment
    dir_path = os.path.join(os.path.dirname(
        os.path.realpath(__file__)), "shared")
    if dir_path not in sys.path:
        sys.path.insert(0, dir_path)
    '''

    return depency_packages


def my_test_suite():
    ''' Sets up the testing
    '''
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('test', pattern='test_*.py')
    return test_suite


if __name__ == "__main__":

    # setup basic extension
    lib_dirs_dyna = []
    libs_dyna = []
    srcs_dyna, include_dirs_dyna, compiler_args_dyna = setup_dyna_cpp()

    # compile binout
    '''
    srcs_dyna, compiler_args_dyna = setup_dyna_cpp_binout(
        srcs_dyna, compiler_args_dyna)
    '''

    # setup hdf5
    # (MUST be before femzip, due to linking)
    '''
    srcs_dyna, \
    compiler_args_dyna, \
    libs_dyna, \
    lib_dirs_dyna, \
    include_dirs_dyna = setup_dyna_cpp_hdf5(srcs_dyna,
                                            compiler_args_dyna,
                                            libs_dyna,
                                            lib_dirs_dyna,
                                            include_dirs_dyna)
    '''

    # setup femzip (if possible)
    srcs_dyna, lib_dirs_dyna, libs_dyna, compiler_args_dyna = setup_dyna_cpp_femzip(
        srcs_dyna,
        lib_dirs_dyna,
        libs_dyna,
        compiler_args_dyna)

    # setup extension
    dyna_extension = Extension("dyna_cpp", srcs_dyna,
                               extra_compile_args=compiler_args_dyna,
                               library_dirs=lib_dirs_dyna,
                               libraries=libs_dyna,
                               include_dirs=include_dirs_dyna,)

    # (3) SETUP
    setup(name='qd',
          version=version,
          license='GNU GPL v3',
          description='QD-Engineering Python Library for CAE',
          author='C. Diez, D. Toewe',
          url='http://www.qd-eng.de',
          author_email='qd.eng.contact@gmail.com',
          packages=(['qd',
                     'qd.cae',
                       'qd.cae.beta',
                       'qd.cae.resources',
                       'qd.numerics',
                     ]),
          package_dir={'qd': 'qd',
                       'qd.cae': 'qd/cae',
                       'qd.cae.beta': 'qd/cae/beta',
                       'qd.cae.resources': 'qd/cae/resources',
                       'qd.numerics': 'qd/numerics',
                       },
          package_data={
              'qd.cae.resources': ['*.js', 'html.template'],
              'qd.cae.beta': ['meta_remote_control', 'meta_remote_control.exe', 'msvcr71.dll']
          },
          ext_package='qd.cae',  # where to place c extensions
          ext_modules=[dyna_extension],
          install_requires=['numpy>=1.8',
                            'diversipy', 'pybind11>=2.2.0', 'h5py'],
          keywords=['cae',
                      'simulation',
                      'engineering',
                      'ls-dyna',
                      'postprocessing',
                      'preprocessing'],
          classifiers=['Development Status :: 4 - Beta',
                       'Programming Language :: C++',
                       'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
                       'Topic :: Scientific/Engineering',
                       'Intended Audience :: Science/Research',
                       'Topic :: Utilities',
                       'Operating System :: Microsoft :: Windows',
                       'Operating System :: POSIX :: Linux',
                       'Programming Language :: Python :: 3.5',
                       'Programming Language :: Python :: 3.6'],
          test_suite='setup.my_test_suite',)
