from setuptools import setup, find_packages

setup(
    name="PasswordGenerator",  # Replace with your package's name
    version="0.1.0",  # Replace with your package's version
    packages=find_packages(),  # This will find all packages in your project
    install_requires=[
        # Your project's dependencies
        "pyperclip",  # Dependency for clipboard operations
        # If you have other dependencies, list them here
    ],
    # Additional metadata about your project
    author="Pierre Gode",  # Replace with your name
    author_email="pierre.gode@example.com",  # Replace with your email
    description="A simple and efficient password generator built with Tkinter.",  # A brief description of your project
    url="http://github.com/PierreGode/PasswordGenerator",  # Replace with your project's URL
    entry_points={
        'console_scripts': [
            'passwordgenerator=password_generator_app:main',  # Adjust with the entry point of your application
        ],
    },
    classifiers=[
        # Classifiers help users find your project by categorizing it.
        # For a list of valid classifiers, see https://pypi.org/classifiers/
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # Specify the minimum version of Python required
)
