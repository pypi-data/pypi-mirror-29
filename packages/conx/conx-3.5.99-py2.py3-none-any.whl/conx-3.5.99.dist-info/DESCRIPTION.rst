Conx Neural Networks
====================

The On-Ramp to Deep Learning
----------------------------

Built in Python 3 on Keras 2.

|Binder| |CircleCI| |codecov| |Documentation Status| |PyPI version|

Read the documentation at
`conx.readthedocs.io <http://conx.readthedocs.io/>`__

Ask questions on the mailing list:
`conx-users <https://groups.google.com/forum/#!forum/conx-users>`__

Implements Deep Learning neural network algorithms using a simple
interface with easy visualizations and useful analytical. Built on top
of Keras, which can use either
`TensorFlow <https://www.tensorflow.org/>`__,
`Theano <http://www.deeplearning.net/software/theano/>`__, or
`CNTK <https://www.cntk.ai/pythondocs/>`__.

The network is specified to the constructor by providing sizes. For
example, Network("XOR", 2, 5, 1) specifies a network named "XOR" with a
2-node input layer, 5-unit hidden layer, and a 1-unit output layer.

Example
-------

Computing XOR via a target function:

.. code:: python

    from conx import Network, SGD

    dataset = [[[0, 0], [0]],
               [[0, 1], [1]],
               [[1, 0], [1]],
               [[1, 1], [0]]]

    net = Network("XOR", 2, 5, 1, activation="sigmoid")
    net.set_dataset(dataset)
    net.compile(error='mean_squared_error',
                optimizer=SGD(lr=0.3, momentum=0.9))
    net.train(2000, report_rate=10, accuracy=1)
    net.test()

Creates dynamic, rendered visualizations like this:

Install
-------

Rather than installing conx, consider using our
`mybinder <https://mybinder.org/v2/gh/Calysto/conx/master?filepath=binder%2Findex.ipynb>`__
in-the-cloud version. Availability may be limited due to demand.

``conx`` requires Python3, Keras version 2.0.8 or greater, and some
other Python modules that are installed automatically with pip.

On Linux, you may need to install ``libffi`` and ``libffi-dev`` in order
to render layers for the network display. If you attempt to display a
network and it appears empty, or if you attempt to
network.propagate\_to\_image() and it gives a PIL error, you need these
libraries.

On Ubuntu or other Debian-based system:

.. code:: bash

    sudo apt install libffi-dev libffi6

Next, we use ``pip`` to install the Python packages.

**Note**: you may need to use ``pip3``, or admin privileges (eg, sudo),
or install into a user environment.

.. code:: bash

    pip install conx -U

You will need to decide whether to use Theano, TensorFlow, or CNTK. Pick
one. See
`docs.microsoft.com <https://docs.microsoft.com/en-us/cognitive-toolkit/Setup-CNTK-on-your-machine>`__
for installing CNTK on Windows or Linux. All platforms can also install
either of the others using pip:

.. code:: bash

    pip install theano

**or**

.. code:: bash

    pip install tensorflow

On MacOS, you may also need to render the SVG visualizations:

.. code:: bash

    brew install cairo

To make MP4 movies, you will need the ``ffmpeg`` executable installed
and available on your default path.

On MacOS, you could use:

.. code:: bash

    brew install ffmpeg

On Windows:

See, for example,
https://github.com/adaptlearning/adapt_authoring/wiki/Installing-FFmpeg

On Linux:

.. code:: bash

    sudo apt install ffmpeg
    # or perhaps:
    sudo yum install ffmpeg

Use with Jupyter Notebooks
--------------------------

To use the Network.dashboard() and camera functions, you will need to
enable ``ipywidgets``:

.. code:: bash

    jupyter nbextension enable --py widgetsnbextension

If you install via conda, then it will already be enabled:

.. code:: bash

    conda install -c conda-forge ipywidgets

Setting the Keras Backend
~~~~~~~~~~~~~~~~~~~~~~~~~

To use a Keras backend other than TensorFlow, edit (or create)
``~/.keras/kerson.json``, like:

.. code:: json

    {
        "backend": "theano",
        "image_data_format": "channels_last",
        "epsilon": 1e-07,
        "floatx": "float32"
    }

Troubleshooting
---------------

#. If you have a problem after installing matplotlib with pip, and you
   already have matplotlib installed (say, with apt) you may want to
   remove the apt-installed version of matplotlib.

Examples
--------

See the `notebooks
folder <https://github.com/Calysto/conx/tree/master/notebooks>`__ and
the `documentation <http://conx.readthedocs.io/en/latest/>`__ for
additional examples.

.. |Binder| image:: https://mybinder.org/badge.svg
   :target: https://mybinder.org/v2/gh/Calysto/conx/master?filepath=binder%2Findex.ipynb
.. |CircleCI| image:: https://circleci.com/gh/Calysto/conx/tree/master.svg?style=svg
   :target: https://circleci.com/gh/Calysto/conx/tree/master
.. |codecov| image:: https://codecov.io/gh/Calysto/conx/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/Calysto/conx
.. |Documentation Status| image:: https://readthedocs.org/projects/conx/badge/?version=latest
   :target: http://conx.readthedocs.io/en/latest/?badge=latest
.. |PyPI version| image:: https://badge.fury.io/py/conx.svg
   :target: https://badge.fury.io/py/conx


