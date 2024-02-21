from setuptools import setup, find_packages

setup(
    name="PierresPasswordGenerator",
    version="1.0.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "pyperclip",  # Add other dependencies as required
    ],
    entry_points={
        "console_scripts": [
            "pierres-password-generator=password_generator_app:main",  # Adjust if necessary
        ]
    },
    author="Pierre Gode",
    author_email="your-email@example.com",  # Replace with your email
    description="A simple Tkinter-based password generator application",
    keywords="password generator tkinter",
    url="http://github.com/PierreGode/PasswordGenerator",  # Replace with the actual URL
    project_urls={
        "Bug Tracker": "http://github.com/PierreGode/PasswordGenerator/issues",  # Replace with the actual URL
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # Adjust the license accordingly
        "Operating System :: OS Independent",
    ],
)

