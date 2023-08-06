# discon
Push python project to pypi and conda server

## Prerequisities

    conda install conda-build anaconda-client
    apt-get install bumpversion


## Install

    conda install -c mjirik -c conda-forge discon


## Required user accounts

### Init PyPI

https://pypi.python.org/pypi

Create `~/.pypirc` with password and login

### Init Anaconda

https://anaconda.org/account/

Login to anaconda:

    binstar login


## Project directory
You will need `setup.py`, `meta.yaml` and `setup.cfg` in your python
project directory. Files can be generated with `init`.
 
There also may be `bld.bat` and `build.sh`. These
files are created if they are not exist.

Conda channels should



## Usage

In new project you can generate `.condarc`, `setup.py`, `setup.cfg` and `meta.yml`

    python -m discon init
    
or

    python -m discon init project_name

Create and upload new patch, minor or major version

    python -m discon patch
    python -m discon minor
    python -m discon major -c some_channel


Push your git `master` branch to `stable` branch

    python -m discon stable


