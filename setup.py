import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

from setuptools.command.develop import develop
from setuptools.command.install import install
from subprocess import check_call
import os


class PostInstallCommand(install):
    def run(self):
        os.system("mkdir -p $CONDA_PREFIX/etc/conda/activate.d")
        os.system("mkdir -p $CONDA_PREFIX/etc/bsstudio")
        os.system('echo "from bsstudio.qtplugins import *"> $CONDA_PREFIX/etc/bsstudio/load_plugin.py')
        os.system('echo "export PYQTDESIGNERPATH=$CONDA_PREFIX/etc/bsstudio"> $CONDA_PREFIX/etc/conda/activate.d/env_vars.sh')

        #os.system("conda install --yes --file requirements.txt")
        #os.system("conda install --yes -c conda-forge/label/cf201901 pyqt")
        #os.system("conda install --yes bluesky -c lightsource2-tag")
        install.run(self)
        
setuptools.setup(
    name="bsstudio",
    version="1.0.1",
    author="Bayan Alexander Sobhani",
    author_email="bsobhani@bnl.gov",
    description="Bluesky widgets for PyQt",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    cmdclass={
        'install': PostInstallCommand,
    },
)
