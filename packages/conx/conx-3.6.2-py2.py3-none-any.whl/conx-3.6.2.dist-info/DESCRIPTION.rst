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

Computing XOR via a target function:

.. code:: python

    import conx as cx

    dataset = [[[0, 0], [0]],
               [[0, 1], [1]],
               [[1, 0], [1]],
               [[1, 1], [0]]]

    net = cx.Network("XOR", 2, 5, 1, activation="sigmoid")
    net.set_dataset(dataset)
    net.compile(error='mean_squared_error',
                optimizer="sgd", lr=0.3, momentum=0.9)
    net.train(2000, report_rate=10, accuracy=1.0)
    net.test(show=True)

Creates dynamic, rendered visualizations like this:

Examples
--------

See
`conx-notebooks <https://github.com/Calysto/conx-notebooks/blob/master/00_Index.ipynb>`__
and the `documentation <http://conx.readthedocs.io/en/latest/>`__ for
additional examples.

Installation
------------

| See `How To Run
  Conx <https://github.com/Calysto/conx-notebooks/tree/master/HowToRun#how-to-run-conx>`__
| to see options on running virtual machines, in the cloud, and personal
| installation.

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


