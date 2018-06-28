import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pySankey",
    version="1.0.0",
    author="anazalea",
    author_email="anneyagolob@gmail.com",
    description="Make simple, pretty Sankey Diagrams",
    long_description=long_description,
    license='GNU General Public License v3.0',
    long_description_content_type="text/markdown",
    url="https://github.com/anazalea/pySankey",
    packages=setuptools.find_packages(),
    install_requires=['matplotlib>=2.1.0rc1',
                      'seaborn>=0.8.1',
                      'numpy>=1.13.3'],
    classifiers=(
        "Programming Language :: Python :: 3",
        'LICENSE :: OSI APPROVED :: GNU AFFERO GENERAL PUBLIC LICENSE V3',
        "Operating System :: OS Independent",
    ),
)
