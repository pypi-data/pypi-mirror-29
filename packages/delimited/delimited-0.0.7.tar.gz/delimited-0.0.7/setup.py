import io
import os
import sys
import shutil
import subprocess
import setuptools


# read metadata
setup_path = os.path.abspath(os.path.dirname(__file__))
metadata_path = os.path.join(setup_path, "delimited", "__init__.py")
metadata = {}
with open(metadata_path) as file_handle:
    exec(file_handle.read(), metadata)


setuptools.setup(
    name=metadata["__title__"],
    version=metadata["__version__"],
    description=metadata["__summary__"],
    keywords="delimited nested",
    url=metadata["__url__"],
    author=metadata["__author__"],
    author_email=metadata["__email__"],
    license=metadata["__license__"],
    packages=["delimited"],
    extras_require={
        "test": ["green", "coverage"],
        "docs": ["sphinx", "sphinx_rtd_theme"]
    },
    classifiers=[
        "Development Status :: 3 - Alpha"
    ]
)
