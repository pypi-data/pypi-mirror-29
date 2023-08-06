EAST Text Detector
==================

We provide a python package for the tensorflow implementation of the text detector presented by Zhou et al.
in their paper "EAST: An Efficient and Accurate Scene Text Detector", CVPR 2017. The code is an adaption of
https://github.com/argman/EAST.

We only wrote a wrapper class and packaged the code, all the logic is taken from the above mentioned github repo.
For any questions or suggestions, please refer to: https://github.com/argman/EAST

Installation
============

* Create a virtual environment:

.. code-block:: bash

    python3 -m venv venv3

* Activate it:

.. code-block:: bash

    source venv3/bin/activate

* Install dependencies with pip:

.. code-block:: bash

    pip3 install lanms

* Install east-detector with pip:

.. code-block:: bash

    pip3 install east-detector
