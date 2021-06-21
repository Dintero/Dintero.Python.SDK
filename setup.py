import os
from codecs import open
from setuptools import setup, find_packages

this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()
version_contents = {}

with open(
    os.path.join(this_directory, "dintero", "version.py"), encoding="utf-8"
) as f:
    exec(f.read(), version_contents)

setup(
    name="dintero",
    version=version_contents["VERSION"],
    description="Python bindings for the Dintero API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Dintero",
    author_email="integration@dintero.com",
    url="https://github.com/dintero/Dintero.Python.SDK",
    license="MIT",
    keywords="dintero api payments",
    packages=find_packages(exclude=["tests", "tests.*"]),
    zip_safe=False,
    install_requires=[
        'requests >= 2.20; python_version >= "3.0"',
        'typing_extensions >= 3.10; python_version >= "3.0"',
    ],
    extras_require={
        "dev": [
            "pytest",
        ]
    },
    python_requires=">=3.6",
    project_urls={
        "Bug Tracker": "https://github.com/dintero/Dintero.Python.SDK/issues",
        "Documentation": "https://docs.dintero.com",
        "Source Code": "https://github.com/dintero/Dintero.Python.SDK",
    },
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
