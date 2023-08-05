.. image:: https://travis-ci.org/ibaidev/bolib.svg?branch=master
  :target: https://travis-ci.org/ibaidev/bolib
  :alt: Build Status
.. image:: https://readthedocs.org/projects/bolib/badge/?version=latest
  :target: http://bolib.readthedocs.io/?badge=latest
  :alt: Documentation Status

BOlib
=====

A python library for Bayesian Optimization.

Setup BOlib
-----------

- The following packages must be installed before installing BOlib

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

  python -m pip install bolib


Use BOlib
---------

- Import BOlib to use it in your python script.

.. code-block:: python

  import bolib

- Some well-known objetive functions have been included.

.. code-block:: python

  of = bolib.ofs.Branin()

  of.evaluate([1.0, 1.0]) # 27.702905548512433


- To use Bayesian Optimization we need a probabilistic model. In this example we will use Gaussian Processes.

.. code-block:: python

  import gplib
  import numpy as np

  # We initialize data before the first evaluation.

  data = {
      'X': np.zeros((2, len(of.get_bounds()))),
      'Y': np.array([[-1.0], [1.0]])
  }

  model = gplib.GP(
      gplib.mea.Constant(data),
      gplib.cov.SquaredExponential(data, is_ard=True),
      gplib.lik.Gaussian(is_noisy=True),
      gplib.inf.ExactGaussian(),
      gplib.fit.HparamOptimization(
          max_fun_call=1000,
          ls_method="Powell",
          max_ls_fun_call=1000,
          save_opt=True
      )
  )


- Bayesian Optimization also needs an acquisition function.

.. code-block:: python

  af = bolib.afs.ExpectedImprovement()


- Finally, we can initialize our optimization model and start the optimization process.

.. code-block:: python

  # We get a random sample within the bounds of the objective function
  seed = 1
  bo = bolib.methods.BayesianOptimization(model, af, seed)

  x0 = bolib.util.random_sample(of.get_bounds(), batch_size=10)

  bo.minimize(
      of.evaluate, x0,
      bounds=of.get_bounds(),
      tol=1e-7,
      maxiter=of.get_max_eval(),
      disp=True
  )

- BOlib is also Scipy compatible.

.. code-block:: python

  import scipy.optimize as spo

  result = spo.minimize(
      of.evaluate,
      x0,
      bounds=of.get_bounds(),
      method=bo.minimize,
      tol=1e-7,
      options={
          'maxiter': of.get_max_eval(),
          'disp': True
      }
  )


- There are more examples in examples/ directory. Check them out!

Develop BOlib
-------------

-  Download the repository using git

.. code-block:: bash

  git clone https://github.com/ibaidev/bolib.git
  cd bolib
  git config user.email 'MAIL'
  git config user.name 'NAME'
  git config credential.helper 'cache --timeout=300'
  git config push.default simple

-  Update API documentation

.. code-block:: bash

  source ./.env/bin/activate
  pip install Sphinx
  cd docs/
  sphinx-apidoc -f -o ./ ../bolib


