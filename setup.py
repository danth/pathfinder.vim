from setuptools import find_packages, setup

__version__ = "3.1.2"


setup(
    name="pathfinder.vim",
    version=__version__,
    author="Daniel Thwaites",
    author_email="danthwaites30@btinternet.com",
    url="https://github.com/danth/pathfinder.vim",
    packages=find_packages(exclude=("tests",)),
)
