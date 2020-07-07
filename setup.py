import setuptools

with open("README.md", "r", encoding="UTF-8") as fh:
    long_description = fh.read()

TEST_REQUIRES = ["pylint", "coverage", "coveralls"]

setuptools.setup(
    name="pySankeyBeta",
    version="1.2.2",
    author="pierre-sassoulas",
    author_email="pierre.sassoulas@gmail.com",
    description="Make simple, pretty Sankey Diagrams (Beta version)",
    long_description=long_description,
    license="GNU General Public License v3.0",
    long_description_content_type="text/markdown",
    url="https://github.com/pierre-sassoulas/pySankey",
    packages=setuptools.find_packages(),
    install_requires=["matplotlib>=2.1.0rc1", "seaborn>=0.8.1", "numpy>=1.13.3"],
    test_requires=TEST_REQUIRES,
    extras_require={"test": TEST_REQUIRES},
    classifiers=(
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: OS Independent",
    ),
)
