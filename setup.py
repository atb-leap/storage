import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="storage",
    version="0.0.1",
    author="Zane McCaig",
    author_email="zmccaig@atb.com",
    description="A python library for getting and saving files locally and in google cloud storage",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/atb-leap/storage",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
