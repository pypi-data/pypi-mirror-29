#setup.py

from setuptools import setup


setup(
    # Application name:
    name="ha_flam",

    # Version number (initial):
    version="0.1.3",

    # Application author details:
    author="Hunter Albaugh",
    author_email="hunteralbaugh@gmail.com",
    description='FreeLanceAssetManager.',
    # Packages
    packages=["FLAM"],

    # Include additional files into the package
    include_package_data=True,

    # Details
    url="https://github.com/halbaugh/FLAM",

    #
    license="LICENSE.txt",

    long_description=open("README.txt").read(),

    # Dependent packages (distributions)
    install_requires=[
        "PySide","sqlalchemy",
    ],
    zip_safe=False
)