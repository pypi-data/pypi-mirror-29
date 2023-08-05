============
waterfurnace
============


.. image:: https://img.shields.io/pypi/v/waterfurnace.svg
   :target: https://pypi.python.org/pypi/waterfurnace

.. image:: https://img.shields.io/travis/sdague/waterfurnace.svg
   :target: https://travis-ci.org/sdague/waterfurnace

.. image:: https://readthedocs.org/projects/waterfurnace/badge/?version=latest
   :target: https://waterfurnace.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

.. image:: https://pyup.io/repos/github/sdague/waterfurnace/shield.svg
   :target: https://pyup.io/repos/github/sdague/waterfurnace/
   :alt: Updates


Python interface for waterfurnace geothermal systems.

This provides basic sensor readings for waterfurnace geothermal systems by
using the websocket interface that exists for the symphony website. This is not
a documented or stable interface, so don't use this for critical
systems. However, it is useful to record historical usage of your waterfurnace
system.


* Free software: Apache Software License 2.0
.. * Documentation: https://waterfurnace.readthedocs.io.


Credits
---------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage


=======
History
=======

0.5.0 (2018-02-16)
------------------

* Update exception handling to be more Home Assistant friendly

0.4.0 (2018-02-05)
------------------

* More exceptions to distinguish errors we are expecting

0.3.0 (2018-01-23)
------------------

* Handle tid rollover

0.2.0 (2018-01-19)
------------------

* Library specific exceptions for login failures.

0.1.0 (2018-01-17)
------------------

* First release on PyPI.


