.. _Introduction:

Introduction
==============
SenSE is a comprehensive community framework designed for radiative transfer (RT) modeling in the active microwave domain.
It summarizes various RT models developed for synthetic aperture radar (SAR) to simulate backscatter responses from open soil and vegetated land surfaces, primarily in agricultural settings.
This integration encompasses different models for scattering and emission across various surfaces, providing a cohesive operational structure.

One of the framework's most significant advantages is its modular design, which allows for the easy substitution and analysis of different surface and canopy scattering models within a single system.
This flexibility facilitates seamless model exchange, enhancing the framework's adaptability and utility.
The SenSE package currently includes several surface models such as Oh92 :cite:`oh_empirical_1992_a`, Oh04 :cite:`yisok_oh_quantitative_2004_a`, Dubois95 :cite:`dubois_measuring_1995_a`, IEM :cite:`fung_backscattering_1992_a`, and the surface component of the Water Cloud Model (WCM) :cite:`attema_vegetation_1978_a`.
For canopy modeling, it supports models like SSRT :cite:`de_roo_semi-empirical_2001_a` :cite:`ulaby_microwave_2014_a` and WCM :cite:`attema_vegetation_1978_a`.

Additionally, the framework incorporates the dielectric mixing model by Dobson et al. :cite:`dobson_microwave_1985_a`, available in various versions for converting soil moisture content to a dielectric constant.
SenSE also includes essential utility functions, such as those for frequency-wavelength conversion and calculating Fresnel reflectivity coefficients, further enhancing its analytical capabilities.

Statement of need
------------------
.. include:: text_blocks_README_RtD/statement_of_need.rst

Getting Started
------------------
Please find instructions on how to download and install SenSE in the :ref:`Installation` section.

.. include:: text_blocks_README_RtD/support_contributing_testing.rst

.. rubric:: References
.. bibliography:: references_01_introduction.bib
    :style: unsrt
    :cited: