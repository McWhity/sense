.. _Introduction:

Introduction
==============
SenSE is a comprehensive community framework designed for radiative transfer (RT) modeling in the active microwave domain.
It summarizes Radiative Transfer (RT) models developed for the active microwave domain (SAR) to simulate backscatter responses from open soil and vegetated (mainly agriculture) land surfaces.
This integration spans different models for scattering and emission across various surfaces, providing a cohesive operational structure.

The framework's modular design is one of its most significant advantages, allowing easy substitution and analysis of different surface and canopy scattering models within a single system.
This flexibility facilitates the seamless exchange of models, enhancing the framework's adaptability and utility.
Currently, the SenSE package includes several surface models such as Oh92 :cite:`oh_empirical_1992`, Oh04 :cite:`yisok_oh_quantitative_2004`, Dubois95 :cite:`dubois_measuring_1995`, IEM :cite:`fung_backscattering_1992`, and the surface component of the Water Cloud Model (WCM) :cite:`attema_vegetation_1978`.
For canopy modeling, it supports models like SSRT :cite:`de_roo_semi-empirical_2001` :cite:`ulaby_microwave_2014` and WCM :cite:`attema_vegetation_1978`.

Additionally, the framework incorporates the dielectric mixing model by Dobson et al. :cite:`dobson_microwave_1985` in various versions for converting soil moisture content to a dielectric constant.
SenSE also includes essential utility functions, such as those for frequency-wavelength conversion and calculating Fresnel reflectivity coefficients, further enhancing its analytical capabilities.

Statement of need
------------------
.. include:: text_blocks_README_RtD/statement_of_need.rst

Getting Started
------------------
Please find instructions on how to download and install SenSE in the :ref:`Installation` section.

.. include:: text_blocks_README_RtD/support_contributing_testing.rst

.. rubric:: References
.. bibliography:: references.bib
    :style: unsrt