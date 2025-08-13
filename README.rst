|Pytest| |Documentation Status| |License: GPL v3| |Discussions|

SenSE: Community SAR ScattEring model
=====================================

SenSE is a generic
community framework for radiative transfer (RT) modelling in the active
microwave domain. It implements different existing models for scattering
and emission for different surfaces in a coherent framework to simulate
SAR backscattering coefficients as function of surface biogeophysical
parameters. In the microwave domain the surface and canopy contribution
of the total backscatter is usually estimated separately. Within the
SenSE framework different model combination of surface and canopy models
can be easily brought together and moreover analyzed. The analysis of
the different model combination within one framework can be seen as the
biggest advantage of the developed SenSE package. Currently implemented
surface models are: Oh1992, Oh2004, Dubois95 and IEM and Water Cloud.
Currently implemented canopy models are: SSRT and Water Cloud.

Statement of need
-----------------
.. include:: docs/text_blocks_README_RtD/statement_of_need.rst

Installation
--------------

Installation with Conda
~~~~~~~~~~~~~~~~~~~~~~~
.. include:: docs/text_blocks_README_RtD/installation_with_conda.rst

Installation via virtualenv and python
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. include:: docs/text_blocks_README_RtD/installation_with_virtualenv.rst

Installation via Docker
~~~~~~~~~~~~~~~~~~~~~~~
.. include:: docs/text_blocks_README_RtD/installation_with_docker.rst

Optional: Installation of further dependencies
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
.. include:: text_block_README_RtD/testing_rtd_jupyter_dependencies.rst

Usage
-----

For usage checkout the `juypter
notebook <https://nbviewer.jupyter.org/github/mcwhity/sense/tree/master/docs/notebooks/>`__

Documentation
-------------

We use `Sphinx <http://www.sphinx-doc.org/en/stable/rest.html>`__ to
generate the documentation of ``SenSE`` on
`ReadTheDocs <https://sense-community-sar-scattering-model.readthedocs.io/en/latest/>`__.


.. include:: text_blocks_README_RtD/installation_with_docker.rst

Authors
-------

.. include:: AUTHORS.rst

License
-------

This project is licensed under the GPLv3 License - see the
`LICENSE.rst <LICENSE.rst>`__ file for details.

.. |Build Status| image:: https://gitlab.uni-rostock.de/mcwhity/sense/badges/master/pipeline.svg
   :target: https://gitlab.uni-rostock.de/mcwhity/sense
.. |Documentation Status| image:: https://readthedocs.org/projects/sense-community-sar-scattering-model/badge/?version=latest
   :target: https://sense-community-sar-scattering-model.readthedocs.io/en/latest/?badge=latest
.. |License: GPL v3| image:: https://img.shields.io/badge/License-GPLv3-blue.svg
   :target: https://www.gnu.org/licenses/gpl-3.0
.. |Pytest| image:: https://github.com/mcwhity/sense/actions/workflows/test_build_pytest.yml/badge.svg?branch=master
   :target: https://github.com/mcwhity/sense/actions/workflows/test_build_pytest.yml
   :alt: Pytest
.. |Discussions| image:: https://img.shields.io/static/v1?label=Discussions&message=Ask&color=blue&logo=github
   :target: https://github.com/mcwhity/sense/discussions