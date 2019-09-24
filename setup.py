import setuptools

try:
    # for pip >= 10
    from pip._internal.req import parse_requirements
except ImportError:
    # for pip <= 9.0.3
    from pip.req import parse_requirements

def load_requirements(fname):
    reqs = parse_requirements(fname, session="test")
    return [str(ir.req) for ir in reqs]

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="storage",
    version="0.0.2",
    author="Zane McCaig",
    author_email="zmccaig@atb.com",
    description="A python library for getting and saving files locally and in google cloud storage",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=load_requirements("requirements.txt"),
    url="https://github.com/atb-leap/storage",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
