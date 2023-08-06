ServeIt
=======

|Build Status| |Codacy Grade Badge| |Codacy Coverage Badge| |PyPI
version|

ServeIt lets you easily serve model predictions and supplementary
information from a RESTful API. Current features include:

1. Model inference serving via RESTful API endpoint
2. Extensible library for inference-time data loading, preprocessing,
   input validation, and postprocessing
3. Supplementary information endpoint creation
4. Automatic JSON serialization of responses
5. Configurable request and response logging (work in progress)

Installation: Python 2.7 and Python 3.6
---------------------------------------

Installation is easy with pip: ``pip install serveit``

Usage:
------

Deploy your model ``clf`` to an API endpoint with as little as one line
of code:

.. code:: python

    from serveit.server import ModelServer

    # initialize server with a model and a method to use for predictions
    # then start serving predictions
    ModelServer(clf, clf.predict).serve()

Your new API is now accepting ``POST`` requests at
``localhost:5000/predictions``! Please see the `examples <examples>`__
directory for additional usage.

Supported libraries
~~~~~~~~~~~~~~~~~~~

-  Scikit-Learn
-  Keras
-  PyTorch

Coming soon:
~~~~~~~~~~~~

-  TensorFlow

Building
--------

You can build locally with: ``python setup.py``

License
-------

`MIT <LICENSE.md>`__

.. |Build Status| image:: https://travis-ci.org/rtlee9/serveit.svg?branch=master
   :target: https://travis-ci.org/rtlee9/serveit
.. |Codacy Grade Badge| image:: https://api.codacy.com/project/badge/Grade/2af32a3840d5441e815f3956659b091f
   :target: https://www.codacy.com/app/ryantlee9/serveit
.. |Codacy Coverage Badge| image:: https://api.codacy.com/project/badge/Coverage/2af32a3840d5441e815f3956659b091f
   :target: https://www.codacy.com/app/ryantlee9/serveit
.. |PyPI version| image:: https://badge.fury.io/py/ServeIt.svg
   :target: https://badge.fury.io/py/ServeIt


