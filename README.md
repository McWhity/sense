[![Pytest](https://github.com/mcwhity/sense/actions/workflows/test_build_pytest.yml/badge.svg?branch=master)](https://github.com/mcwhity/sense/actions/workflows/test_build_pytest.yml)
[![Documentation
Status](https://readthedocs.org/projects/sense-community-sar-scattering-model/badge/?version=latest)](https://sense-community-sar-scattering-model.readthedocs.io/en/latest/?badge=latest)
[![License: GPL
v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Discussions](https://img.shields.io/static/v1?label=Discussions&message=Ask&color=blue&logo=github)](https://github.com/mcwhity/sense/discussions)

# SenSE: Community SAR ScattEring model

SenSE is a generic community framework for radiative transfer (RT)
modelling in the active microwave domain. It implements different
existing models for scattering and emission for different surfaces in a
coherent framework to simulate SAR backscattering coefficients as
function of surface biogeophysical parameters. In the microwave domain
the surface and canopy contribution of the total backscatter is usually
estimated separately. Within the SenSE framework different model
combination of surface and canopy models can be easily brought together
and moreover analyzed. The analysis of the different model combination
within one framework can be seen as the biggest advantage of the
developed SenSE package. Currently implemented surface models are:
Oh1992, Oh2004, Dubois95 and IEM and Water Cloud. Currently implemented
canopy models are: SSRT and Water Cloud.

## Statement of need

Over the last several decades, various (empirical to physically based)
RT models in the active microwave domain have been developed, tested,
and further modified. However, an easy-to-use framework combining the
most common microwave RT models (simulating backscatter responses of
active microwave sensors) is lacking. Thus, every researcher must
produce their own code implementation from the original source. This
Python framework aims to serve as a first attempt to combine the most
common active microwave-related RT models in a modular way. As a result,
surface and volume scattering models can be easily exchanged with one
another. Such a modular framework provides an opportunity to easily plug
and play with different RT model combinations for various research
questions and use cases. SenSE facilitates the application of RT models,
especially for comparative analysis. Over time, the framework is
expected to grow, incorporating more RT models (e.g., passive microwave
domain) and supplementary functions (e.g., more dielectric mixing
models).

## Installation

### Installation with Conda

Download and install
[Anaconda](https://www.anaconda.com/products/individual) or
[Miniconda](https://docs.conda.io/en/latest/miniconda.html).
Anaconda/Miniconda installation instructions can be found
[here](https://conda.io/projects/conda/en/latest/user-guide/install/linux.html#install-linux-silent)

To install all required modules, use:

    git clone https://github.com/McWhity/sense.git
    cd sense
    conda env create --prefix ./env --file environment.yml
    conda activate ./env # activate the environment

To install SenSE into an existing Python environment, use:

    python -m pip install .

To install for development, use:

    python -m pip install --editable .

### Installation via virtualenv and python

Install system requirements:

    sudo apt install python3-pip python3-tk python3-virtualenv python3-venv virtualenv

Create a virtual environment:

    git clone https://github.com/McWhity/sense.git
    cd sense
    virtualenv -p /usr/bin/python3 env
    source env/bin/activate # activate the environment
    pip install --upgrade pip setuptools # update pip and setuptools

To install SenSE into an existing Python environment, use:

    python -m pip install .

To install for development, use:

    python -m pip install --editable .

### Installation via Docker

SenSE can also be run using Docker. To build it locally use :

    git clone https://github.com/McWhity/sense.git
    cd sense
    docker build -t sense:latest . 

## Usage

For usage checkout the [juypter
notebook](https://nbviewer.jupyter.org/github/mcwhity/sense/tree/master/docs/notebooks/)

## Documentation

We use [Sphinx](http://www.sphinx-doc.org/en/stable/rest.html) to
generate the documentation of `SenSE` on
[ReadTheDocs](https://sense-community-sar-scattering-model.readthedocs.io/en/latest/).

## Authors

-   Alexander Löw (✝ 2 July 2017)
-   Thomas Weiß \<\"<thomas.weiss@uni-rostock.de>\"\>

## License

This project is licensed under the GPLv3 License - see the
[LICENSE.rst](LICENSE.rst) file for details.
