ServeIt
=======

|Build Status| |Codacy Badge| |Codacy Badge| |PyPI version| |License|

ServeIt lets you deploy your models to a RESTful API for prediction
serving in one line of code. Current features include:

1. Model prediction serving
2. Supplementary information endpoint creation
3. Input validation and exception handling
4. Configurable request and response logging (work in progress)

Installation: Python 2.7 and Python 3.6
---------------------------------------

Installation is easy with pip: ``pip install serveit``

Usage:
------

Deploy your model to a production-quality API with one line of code:

.. code:: python

    from serveit.sklearn_server import SklearnServer

    # provide the server with a model and tell it which
    # method to use for predictions
    SklearnServer(clf, clf.predict).serve()

Then check out your new API:

.. code:: bash

    curl -XPOST 'localhost:5000/predictions'\
        -H "Content-Type: application/json"\
        -d "[[5.6, 2.9, 3.6, 1.3], [4.4, 2.9, 1.4, 0.2], [5.5, 2.4, 3.8, 1.1], [5.0, 3.4, 1.5, 0.2], [5.7, 2.5, 5.0, 2.0]]"
    # [1, 0, 1, 0, 2]

Please see the `examples <examples>`__ directory for additional usage
samples.

Supported libraries
-------------------

-  Scikit-Learn

Coming soon:
------------

-  TensorFlow
-  Keras
-  PyTorch

.. |Build Status| image:: https://travis-ci.org/rtlee9/serveit.svg?branch=master
   :target: https://travis-ci.org/rtlee9/serveit
.. |Codacy Badge| image:: https://api.codacy.com/project/badge/Grade/2af32a3840d5441e815f3956659b091f
   :target: https://www.codacy.com/app/ryantlee9/serveit
.. |Codacy Badge| image:: https://api.codacy.com/project/badge/Coverage/2af32a3840d5441e815f3956659b091f
   :target: https://www.codacy.com/app/ryantlee9/serveit
.. |PyPI version| image:: https://badge.fury.io/py/ServeIt.svg
   :target: https://badge.fury.io/py/ServeIt
.. |License| image:: https://img.shields.io/badge/license-MIT-blue.svg
   :target: LICENSE


