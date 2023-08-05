=====
worms
=====


.. image:: https://img.shields.io/pypi/v/worms.svg
        :target: https://pypi.python.org/pypi/worms

.. image:: https://img.shields.io/travis/willsheffler/worms.svg
        :target: https://travis-ci.org/willsheffler/worms

.. image:: https://readthedocs.org/projects/worms/badge/?version=latest
        :target: https://worms.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/willsheffler/worms/shield.svg
     :target: https://pyup.io/repos/github/willsheffler/worms/
     :alt: Updates



Protein Origami via Genetic Fusions


.. image:: https://lh5.googleusercontent.com/9OQLQnMD1IRah4lSRZtROkiLuabY6oclGnGhkGJhsT-gfiFBo_uAQyu-EOxRXziC75iiMpPkTBxmYxE214Si=w2177-h1945
    :width: 300px


* Free software: Apache Software License 2.0
* Documentation: https://worms.readthedocs.io.


Features
--------

please send angry emails to willsheffler@gmail.com until there are docs here.

Credits
---------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage



=======
History
=======

0.1.13 (2018-16-08)
------------------

* raise exception if system too large

0.1.12 (2018-16-08)
------------------

* partial bignum fix

0.1.11 (2018-15-08)
------------------

* fix memory bug
* make distribution work better
* maybe fix pose bug, still some logic err, but maybe ok

0.1.10 (2018-14-08)
------------------

* add max_results option to grow
* fix C2 sym bug
* fix xform axis cen bug
* fix memory "bug" with batch parallel processing

0.1.9 (2018-02-08)
------------------

* add max_samples option to grow

0.1.8 (2018-02-07)
------------------

* origin_seg bug fix

0.1.6 (2018-02-01)
------------------

* middle-to-end cyclic fusions working
* add pretty logo of mid-to-end C3 fusion

0.1.6 (2018-02-01)
------------------

* bug fix in fullatom option

0.1.5 (2018-02-01)
------------------

* add fullatom option to Worms.sympose
* cyclic premutation working for simple beginning-to-end case

0.1.4 (2018-02-01)
------------------

* pypi deplolment derp

0.1.3 (2018-02-01)
------------------

* pypi deplolment derp

0.1.2 (2018-01-23)
------------------

* Add __main__ for module to run tests
* move worms.pdb to worms.data because pdb is kinda reserved
* move utility stuff to util.py
* add some interactive visualization utils for debugging

0.1.1 (2018-01-23)
------------------

* First release on PyPI.


