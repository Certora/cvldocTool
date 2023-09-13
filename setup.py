from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

NAME = "CVLDoc"
VERSION = "2.0.0"

if __name__ == "__main__":
    setup(
        name=NAME,
        version=VERSION,
        author="Certora ltd",
        author_email="support@certora.com",
        description="Utility for reading CERTORA spec files, parse and export their CVLDoc comments to JSON files.",
        long_description=long_description,
        long_description_content_type="text/markdown",
        keywords='Certora CVLDoc',
        url="https://github.com/Certora/cvldocTool",
        packages=find_packages('src'),
        package_dir={'': 'src'},
        include_package_data=True,
        install_requires=[
            'cvldoc_parser==2.0.0',
            'inflection',
            'loguru',
        ],
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
            "Development Status :: 3 - Alpha",
        ],
        python_requires='>=3.7',
        entry_points={
            "console_scripts": [
                "cvldoc=cvldoc_to_json:entry_point",
            ],
        },
    )
