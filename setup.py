from setuptools import setup, find_packages

setup(
    name="PasswordGenerator",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pyperclip",
    ],
    entry_points={
        'gui_scripts': [
            'passwordgenerator=PasswordGenerator:main',
        ],
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="A simple and efficient password generator application built with Tkinter.",
    url="http://github.com/YourUsername/PasswordGenerator",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
