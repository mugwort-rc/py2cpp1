#! /usr/bin/env python

from setuptools import setup

# c++
from distutils.core import Extension

libraries = ['boost_python', 'stdc++']

# py2cpp.util.tuple_parser
tuple_parser = Extension(
    name='py2cpp.util.tuple_parser',
    libraries=libraries,
    sources=['src/tuple_parser/main.cpp'],
    extra_compile_args=['-std=c++11']
)


# distutils c++ bug fix.
import os
from distutils.sysconfig import get_config_vars
(opt,) = get_config_vars('OPT')
os.environ['OPT'] = " ".join(
    [flag for flag in opt.split() if flag != '-Wstrict-prototypes']
)


setup(
    name="py2cpp",
    version="0.1.0",
    description="A translator to translate implicitly statically typed Python code into human-readable C++ code.",
    long_description=open("README.rst").read(),
    license="Apache License (2.0)",
    author="mugwort_rc",
    author_email="mugwort.rc@gmail.com",
    url="https://github.com/mugwort-rc/py2cpp",
    packages=["py2cpp"],
    package_dir={"py2cpp": "src/py2cpp"},
    platforms=["any"],
    include_package_data=True,
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: C++",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Software Development :: Compilers",
    ],
    ext_modules=[tuple_parser]
)
