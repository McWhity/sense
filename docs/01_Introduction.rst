.. _Introduction:

Introduction
==============
SenSE is a comprehensive community framework designed for radiative transfer (RT) modeling in the active microwave domain.
It summarizes various RT models developed for synthetic aperture radar (SAR) to simulate backscatter responses from open soil and vegetated land surfaces, primarily in agricultural settings.
This integration encompasses different models for scattering and emission across various surfaces, providing a cohesive operational structure.

One of the framework's most significant advantages is its modular design, which allows for the easy substitution and analysis of different surface and canopy scattering models within a single system.
This flexibility facilitates seamless model exchange, enhancing the framework's adaptability and utility.
The SenSE package currently includes several surface models such as Oh92 [@oh_empirical_1992], Oh04 [@yisok_oh_quantitative_2004], Dubois95 [@dubois_measuring_1995], IEM [@fung_backscattering_1992], and the surface component of the Water Cloud Model (WCM) [@attema_vegetation_1978].
For canopy modeling, it supports models like SSRT [@de_roo_semi-empirical_2001, @ulaby_microwave_2014] and WCM [@attema_vegetation_1978].

Additionally, the framework incorporates the dielectric mixing model by Dobson et al. [@dobson_microwave_1985], available in various versions for converting soil moisture content to a dielectric constant.
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