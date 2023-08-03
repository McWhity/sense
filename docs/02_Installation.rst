.. _Installation:

Installation for Linux (tested with Ubuntu 22.04)
==================================================
.. note::
    The SenSE has been developed against Python 3.10.
    It cannot be guaranteed to work with previous Python versions.

The first step is to clone the latest code and step into the check out directory::

    git clone https://github.com/McWhity/sense.git
    cd sense

Installation with Conda
------------------------
Download and install `Anaconda <https://www.anaconda.com/products/individual>`_ or `Miniconda <https://docs.conda.io/en/latest/miniconda.html>`_. Anaconda/Miniconda installation instructions can be found `here <https://conda.io/projects/conda/en/latest/user-guide/install/linux.html#install-linux-silent>`_

To install all required modules, use::

    conda env create --prefix ./env --file environment.yml
    conda activate ./env # activate the environment

To install SenSE into an existing Python environment, use::

    python setup.py install

To install for development, use::

    python setup.py develop

Installation with virtualenv and python
----------------------------------------
Install system requirements::

    sudo apt install python3-pip python3-tk python3-virtualenv python3-venv virtualenv

Create a virtual environment::

    virtualenv -p /usr/bin/python3 env
    source env/bin/activate # activate the environment
    pip install --upgrade pip setuptools # update pip and setuptools

To install SenSE into an existing Python environment, use::

    python setup.py install

To install for development, use::

    python setup.py develop


Further information
-------------------

.. literalinclude:: ./environment.yml

Please see the `environment file <https://github.com/McWhity/sense/blob/master/environment.yml>`_ for a list of all installed dependencies during the installation process.

