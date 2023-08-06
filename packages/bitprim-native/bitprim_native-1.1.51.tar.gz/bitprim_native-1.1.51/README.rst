|travis| |appveyor|

bitprim
=======

Bitcoin (and Litecoin) development platform for Python applications

Getting started 
---------------

Stable version:

.. code-block:: bash

    $ pip install --upgrade bitprim-native

Development version:

.. code-block:: bash

    $ pip install --upgrade --index-url https://test.pypi.org/pypi/ bitprim-native


If you want a fully optimized binary for a specific microarchitecture, for example:

.. code-block:: bash

    $ pip install --upgrade --install-option="--microarch=skylake" bitprim-native

(use :code:`--index-url https://test.pypi.org/pypi/` for Dev version)


Reference documentation
-----------------------

For more detailed documentation, please refer to `<https://www.bitprim.org/>`_.


.. |travis| image:: https://travis-ci.org/bitprim/bitprim.svg?branch=master
 		   :target: https://travis-ci.org/bitprim/
 		   
.. |appveyor| image:: https://ci.appveyor.com/api/projects/status/github/bitprim/bitprim?branch=master&svg=true
  		     :target: https://ci.appveyor.com/project/hanchon/bitprim?branch=master

.. role:: bash(code)
   :language: bash