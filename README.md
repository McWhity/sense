
[![Build Status](https://gitlab.uni-rostock.de/mcwhity/sense/badges/master/pipeline.svg)](https://gitlab.uni-rostock.de/mcwhity/sense)
[![Documentation Status](https://readthedocs.org/projects/sense-community-sar-scattering-model/badge/?version=latest)](https://sense-community-sar-scattering-model.readthedocs.io/en/latest/?badge=latest)
<!-- [//]: # ([![DOI]&#40;https://joss.theoj.org/papers/]&#40;https://doi.org/;) -->
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

# SenSE: Community SAR ScattEring model
sense-community-sar-scattering-model.readthedocs.io
SenSE is a generic community framework for radiative transfer (RT) modelling in the active microwave domain. It implements different existing models for scattering and emission for different surfaces in a coherent framework to simulate SAR backscattering coefficients as function of surface biogeophysical parameters. In the microwave domain the surface and canopy contribution of the total backscatter is usually estimated separately. Within the SenSE framework different model combination of surface and canopy models can be easily brought together and moreover analyzed. The analysis of the different model combination within one framework can be seen as the biggest advantage of the developed SenSE package. Currently implemented surface models are: Oh1992, Oh2004, Dubois95 and IEM and Water Cloud. Currently implemented canopy models are: SSRT and Water Cloud.

Within the MULTIPLY project the implemented rt-models will be used for the retrieval of biophysical parameters from the microwave remote sensing data. 

# References
Attema, E.P.W. and Ulaby, F.T., 1978. Vegetation modeled as a water cloud. Radio science, 13(2), pp.357-364.

Dubois, P.C., Van Zyl, J. and Engman, T., (1995). Measuring soil moisture with imaging radars. IEEE Transactions on Geoscience and Remote Sensing, 33(4), pp.915-926.

Oh, Y., Sarabandi, K. and Ulaby, F.T., (1992). An empirical model and an inversion technique for radar scattering from bare soil surfaces. IEEE transactions on Geoscience and Remote Sensing, 30(2), pp.370-381.

Oh, Y., (2004). Quantitative retrieval of soil moisture content and surface roughness from multipolarized radar observations of bare soil surfaces. IEEE Transactions on Geoscience and Remote Sensing, 42(3), pp.596-601.

Ulaby, F.T., Sarabandi, K., McDonald, K., Whitt, M., Dobson, M.C. (1990): Michigan microwave canopy scattering model (MIMICS). Int. J. Remote Sensing. Vol. 11 (7). pp. 1223-1253.

Ulaby, F. T. and D. G. Long, 2014. Microwave Radar and Radiometric Remote Sensing, University of Michigan Press 

