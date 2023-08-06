================================
Data Rhapsody UniversityHack2018
================================


.. image:: https://img.shields.io/pypi/v/universityhack2018.svg
        :target: https://pypi.python.org/pypi/universityhack2018

.. image:: https://img.shields.io/travis/cabadsanchez/universityhack2018.svg
        :target: https://travis-ci.org/cabadsanchez/universityhack2018

.. image:: https://readthedocs.org/projects/universityhack2018/badge/?version=latest
        :target: https://universityhack2018.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status




Package for Data Rhapsody's UniversityHack 2018 Challenge solution.


* Free software: MIT license
* Documentation: https://universityhack2018.readthedocs.io.


Usage
-----

.. code-block:: python
    from universityhack2018.feature_engineering import FeatureEngineering
    from universityhack2018.prediction import Model
    import pandas as pd

    clients_df = pd.read_csv('/path/to/Dataset_Salesforce_Predictive_Modelling_TEST.txt')
    clients = client_df_train.iloc[0:5, :]

    model = Model(clients)
    predictions = model.predict(as_df=True)

    print(predictions.head())

    # Output:
    #   ID_Customer        PA_Est
    # 0    TE000001  26926.541016
    # 1    TE000002  15267.800781
    # 2    TE000003  19499.935547
    # 3    TE000004  12799.532227
    # 4    TE000005  11262.253906

Features
--------

* TODO

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage


=======
History
=======

0.1.0 (2018-03-11)
------------------

* First release on PyPI.


