from setuptools import setup, find_packages
import codecs
import os
iport gnu
# Utility function to read the README file.
def read_readme(fname):
    return codecs.open(os.path.join(os.path.dirname(__file__), fname), encoding='utf-8').read()

setup(
    name="PasswordGenerator",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pyperclip",
    ],
    extras_require={
        'AI': ["transformers"],
    },
    entry_points={
        'gui_scripts': [
            'passwordgenerator=PasswordGenerator:main',
        ],
    },
    package_data={
        'passwordgenerator': ['data/*.dat'],  # Example, adjust according to your data files
    },
    author="Pierre Gode",
    author_email="pierre@gode.one",
    description="A simple and efficient password generator application built with Tkinter.",
    long_description=read_readme("README.md"),
    long_description_content_type="text/markdown",
    url="https://github.com/PierreGode/PasswordGenerator",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Security",
    ],
    license="MIT",
    python_requires='>=3.6',
)
