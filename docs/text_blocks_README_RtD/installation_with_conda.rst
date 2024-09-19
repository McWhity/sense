Download and install `Anaconda <https://www.anaconda.com/products/individual>`_ or `Miniconda <https://docs.conda.io/en/latest/miniconda.html>`_. Anaconda/Miniconda installation instructions can be found `here <https://conda.io/projects/conda/en/latest/user-guide/install/linux.html#install-linux-silent>`_

To install all required modules, use::

    git clone https://github.com/McWhity/sense.git
    cd sense
    conda env create --prefix ./env --file environment.yml
    conda activate ./env # activate the environment

To install SenSE into an existing Python environment, use::

    python setup.py install

To install for development, use::

    python setup.py develop