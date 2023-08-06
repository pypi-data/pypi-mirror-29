import os
from setuptools import setup, find_packages

with open("./configs/requirements.txt", "r") as f:
  dep_packages = f.readlines()
  # remove local install.
  dep_packages = [x.strip() for x in dep_packages if not x.startswith("-e")]

setup(
    name="projectowl",
    version="0.3.11",
    description="Utility library for building python app",
    url="https://flyfj@bitbucket.org/flyfj/owl.git",
    author="Jie Feng",
    author_email="jiefengdev@gmail.com",
    packages=find_packages("./"),
    install_requires=dep_packages,
    include_package_data=True,
    zip_safe=False)
