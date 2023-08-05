ServeIt
=======

ServeIt deploys your trained models to a RESTful API for prediction
serving. Current features include:

1. Model prediction serving
2. Model info endpoint creation
3. Logging

Supported libraries
-------------------

-  Scikit-Learn

.. code:: python

    from sklearn.datasets import load_iris
    from sklearn.linear_model import LogisticRegression
    from serveit.sklearn_server import SklearnServer

    # fit a model on the Iris dataset
    data = load_iris()
    reg = LogisticRegression()
    reg.fit(data.data, data.target)

    # deploy model to a SkLearnServer
    eds = SklearnServer(reg, reg.predict)

    # add informational endpoints
    eds.create_model_info_endpoint()
    eds.create_info_endpoint('features', data.feature_names)
    eds.create_info_endpoint('target_labels', data.target_names.tolist())

    # start API
    eds.serve()

Limited functionality
---------------------

-  TensorFlow
-  Keras
-  PyTorch


