from os import path

from setuptools import setup, find_packages

with open(path.join(path.abspath(path.dirname(__file__)), 'README'), encoding='utf-8') as f:
    long_description = f.read()
with open(path.join(path.abspath(path.dirname(__file__)), 'VERSION'), encoding='utf-8') as f:
    version = f.read()
with open(path.join(path.abspath(path.dirname(__file__)), 'LICENSE'), encoding='utf-8') as f:
    license = f.read()

setup(
    name="kaze",
    description="CLI for Managing The Data Dependency of Deep Learning Projects",
    long_description=long_description,
    version=version,
    url="https://github.com/geyang/dew",
    author="Ge Yang",
    author_email="yangge1987@gmail.com",
    license=license,
    keywords=["datasets", "data", "data science"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3"
    ],
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'kaze = kaze.kaze_cli:kaze'
        ]
    },
    install_requires=[
        "click",
        "pyyaml",
        "termcolor",
        "functional_notations",
        "requests",
        "params-proto"
    ]
)
