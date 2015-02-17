#! /usr/bin/env python

from setuptools import setup

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
    platforms=["any"],
    package_data={"": ["LICENSE", "README.rst"]},
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
)
