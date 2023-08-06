=======
EZedCfg
=======


A basic configuration loading package
-------------------------------------

.. image:: https://img.shields.io/pypi/v/ezedcfg.svg
        :target: https://pypi.python.org/pypi/ezedcfg

.. image:: https://img.shields.io/travis/stephenflynn/ezedcfg.svg
        :target: https://travis-ci.org/stephenflynn/ezedcfg

.. image:: https://readthedocs.org/projects/ezedcfg/badge/?version=latest
        :target: https://ezedcfg.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/stephenflynn/ezedcfg/shield.svg
     :target: https://pyup.io/repos/github/stephenflynn/ezedcfg/
     :alt: Updates



This package's primary purpose is to make it easier to change a programs default
configuration by loading a custom configuration file in either YAML format or
JSON Format.

It does this by performing a dictionary update on a supplied default
configuration.




Installation
------------
.. code-block:: bash

    pip install ezedcfg


Usage
--------

.. code-block::

    from ezedcfg import EZedCfg

    default_configuration = {'item 1' : 1, 'item 2': False}
    path_to_config = 'path/config.yml'

    ezcfg = EZedCfg(default_configuration, path_to_config)

    updated_configuration = ezcfg.load()


If you intend using a json configuration file, add json to the object arguments:

.. code-block::

    ezcfg = EZedCfg(default_configuration, path_to_config,'json')


* Free software: MIT license
* Documentation: https://ezedcfg.readthedocs.io.



Credits
---------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage



=======
History
=======

0.1.5 (2017-09-20)
------------------
0.1.4 (2017-09-20)
------------------

* Sundry fixes to allow Travis.ci to push a build to PyPi.

0.1.3 (2017-09-20)
------------------

* Bugfix v2 for testing on python 3.3 and 3.4.

0.1.2 (2017-09-20)
------------------

* Bugfix for testing on python 3.3 and 3.4.


0.1.0 (2017-09-18)
------------------

* First release on PyPI.


