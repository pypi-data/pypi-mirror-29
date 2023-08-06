.. image:: https://travis-ci.org/ibaidev/gplib.svg?branch=master
  :target: https://travis-ci.org/ibaidev/gplib
  :alt: Build Status
.. image:: https://readthedocs.org/projects/gplib/badge/?version=latest
  :target: http://gplib.readthedocs.io/?badge=latest
  :alt: Documentation Status

GPlib
=====

A python library for Gaussian Process Regression.

Setup GPlib
-----------

- The following packages must be installed before installing GPlib

.. code-block:: bash

  # for ptyhon3
  apt-get install python3-tk
  # or for python2
  apt-get install python-tk

- Create and activate virtualenv (for python2) or
  venv (for ptyhon3)

.. code-block:: bash

  # for ptyhon3
  python3 -m venv --system-site-packages .env
  # or for python2
  virtualenv --system-site-packages .env

  source .env/bin/activate

- Upgrade pip

.. code-block:: bash

  # for ptyhon3
  python3 -m pip install --upgrade pip
  # or for python2
  python -m pip install --upgrade pip

- Install GPlib package

.. code-block:: bash

  python -m pip install gplib


Use GPlib
----------------------

- Generate some random data.

.. code-block:: python

  import numpy as np
  data = {
    'X': np.arange(3, 8, 1.0)[:, None],
    'Y': np.random.uniform(0, 2, 5)[:, None]
  }


- Import GPlib to use it in your python script.

.. code-block:: python

  import gplib

- Initialize the GP with the desired modules.

.. code-block:: python

  gp = gplib.GP(
    mean_function=gplib.mea.Constant(data),
    covariance_function=gplib.cov.SquaredExponential(data, is_ard=False),
    likelihood_function=gplib.lik.Gaussian(is_noisy=True),
    inference_method=gplib.inf.ExactGaussian()
  )


- Plot the GP and the data.

.. code-block:: python

  gplib.plot.gp_1d(gp, data)


- Get the posterior GP given the data.

.. code-block:: python

  posterior_gp = gp.get_posterior(data)


- Finally plot the posterior GP.

.. code-block:: python

  gplib.plot.gp_1d(posterior_gp, data)

- There are more examples in examples/ directory. Check them out!

Develop GPlib
-------------

-  Download the repository using git

.. code-block:: bash

  git clone https://github.com/ibaidev/gplib.git
  cd gplib
  git config user.email 'MAIL'
  git config user.name 'NAME'
  git config credential.helper 'cache --timeout=300'
  git config push.default simple

-  Update API documentation

.. code-block:: bash

  source ./.env/bin/activate
  pip install Sphinx
  cd docs/
  sphinx-apidoc -f -o ./ ../gplib


