Locality-Aware Non-Maximum Suppression (LANMS)
==============================================

We provide a python package for the compiled version of the LANMS as described by Zhout et al.
in their paper "EAST: An Efficient and Accurate Scene Text Detector", CVPR 2017. The code is from the TensorFlow
implementation available on: https://github.com/argman/EAST

We only packaged the code. For any questions or suggestions, please refer to: https://github.com/argman/EAST

Installation
============

* Create a virtual environment:

.. code-block:: bash

    python3 -m venv venv3

* Activate it:

.. code-block:: bash

    source venv3/bin/activate

* Install lanms with pip:

.. code-block:: bash

    pip3 install lanms

Packaging for Linux
===================

* You need to use manylinux: https://github.com/pypa/manylinux

* Install the docker: https://docs.docker.com/install/

* Get the container:

.. code-block:: bash

    docker pull quay.io/pypa/manylinux1_x86_64

*

* From the repository root, call:

.. code-block:: bash

    python setup.py bdist_wheel
