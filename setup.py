import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r") as fh:
    require = fh.readlines()
require = [x.strip() for x in require]

setuptools.setup(
    name="pySankeyBeta",
    version="1.0.4",
    author="pierre-sassoulas",
    author_email="pierre.sassoulas@gmail.com",
    description="Make simple, pretty Sankey Diagrams (Beta version)",
    long_description=long_description,
    license="GNU General Public License v3.0",
    long_description_content_type="text/markdown",
    url="https://github.com/pierre-sassoulas/pySankey",
    packages=setuptools.find_packages(),
    install_requires=require,
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: OS Independent",
    ),
)
