Install system requirements::

    sudo apt install python3-pip python3-tk python3-virtualenv python3-venv virtualenv

Create a virtual environment::

    git clone https://github.com/McWhity/sense.git
    cd sense
    virtualenv -p /usr/bin/python3 env
    source env/bin/activate # activate the environment
    pip install --upgrade pip setuptools # update pip and setuptools

To install SenSE into an existing Python environment, use::

    python -m pip install .

To install for development, use::

    python -m pip install --editable .