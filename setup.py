from setuptools import setup, find_packages

# Specify your main script and options for py2app here
APP = ['PasswordGenerator.py']  
OPTIONS = {
    'argv_emulation': True,
    # Add any other py2app options you need here
}

setup(
    name="PasswordGenerator",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pyperclip",
        # Add other dependencies here
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
    options={'py2app': OPTIONS},  # py2app options
    app=APP,  # py2app target
    # Add any other necessary configuration for your package
)