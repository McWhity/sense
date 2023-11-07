---
title: 'SenSE: Community SAR ScattEring model'
tags:
  - Python
  - SAR
  - radiative transfer
authors:
  - name: Thomas Weiß
    orcid: 0000-0001-5278-8379
    affiliation: 1,2,3
  - name: Alexander Löw
    affiliation: 1
affiliations:
 - name: Department of Geography, Ludwig-Maximilians-Universität München, 80333 Munich, Germany
   index: 1
 - name: Geodesy and Geoinformatics, University of Rostock, Justus-von-Liebig-Weg 6, 18059 Rostock, Germany
   index: 2
 - name: Fraunhofer Institute for Computer Graphics Research IGD, Joachim-Junigus-Straße 11, 18059 Rostock, Germany
   index: 3
date: 28 June 2023
bibliography: paper.bib
---

# Summary
SenSE is a generic community framework for radiative transfer (RT) modelling in the active microwave domain.
It implements different existing RT models for scattering and emission for different surfaces in a coherent framework
to simulate SAR backscattering coefficients as function of surface biogeophysical parameters.
Within the SenSE framework different RT model combination of surface and volume scatting models are brought together
(modular design), thus surface and volume scattering models can be easily exchanged. The easy exchange and analysis 
of the different model combination within one framework can be seen as the biggest advantage of the developed 
SenSE package. Currently implemented surface models are: Oh92 [@oh_empirical_1992], 
Oh04 [@yisok_oh_quantitative_2004], Dubois95 [@dubois_measuring_1995] and IEM [@fung_backscattering_1992] 
and Water Cloud Model (surface part) [@attema_vegetation_1978]. 
Currently available canopy models are: SSRT [@de_roo_semi-empirical_2001,@ulaby_microwave_2014] and 
WCM [@attema_vegetation_1978].
Additionally, for conversion of soil moisture content to a dielectric constant, the dielectric mixing model of 
Dobson et al. [@dobson_microwave_1985] (different versions) is implemented as well.
Furthermore, necessary utility functions like frequency-wavelength conversion or Fresnel reflectivity coefficients are
part of the SenSE framework.
Detailed information are given in RtD and the original source of each model.

Include graphic
Auflistung von allen RT modellen

Surface-scattering RT models

Volume-scattering RT models

Dielectric mixing models for soils

# Statement of need
Over the last decades several different (empirical to physical based) RT models in the active microwave domain 
were developed, tested and further modified. 
But a easy usable framework combing the most common microwave RT models (simulating backscatter 
response of active microwave sensors) is missing.
Thus, every researcher has to produce their own code implementation from the original source.
This python framework shall serve as a first attempt to combine most common active microwave related RT
models in a modular way.
Thus, surface and volume scattering models can be easily exchanged by each other.
Such a modular framework reveals an opportunity to easily plug and play with different RT model combinations for
different research questions and use cases.
SenSE, facilitates the application of RT models, especially for comparative analysis. 
In time, the framework is expected to grow, thus including more and more RT models
(e.g., passive microwave domain) and sublimentary functions (e.g., more dielectric mixing models).

# Applications
The python framework was used within the EU sponsored MULTIPLY Project (https://cordis.europa.eu/project/id/687320) 
with its MULTIPLY platform (https://multiply.obs-website.eu-de.otc.t-systems.com).
Furthermore, the RT models implementation in SenSE was an important asset for the analysis carried out in 
publications [@weis_evaluation_2020,@weis_sentinel-1_2021].
Further, collaboration with researcher in the field of vegetation optical depths in forest areas are ongoing.
Thus, the SenSE functionality will be further used and further extensions of SenSE are to be expected. 

# Other available software scripts (Ulaby and Long code library)

Ulaby and Long wrote an extensive book about the fundamentals of microwave remote sensing.
They provided a ton of matlab codes for demonstration purposes.
But, as the matlab codes are individual code snippets of different RT models, it is not easy to plug and play
with different RT model combinations.
The interactive version of the matlab codes are good for demonstration purposes, but they lack the option to process  
own large datasets.
The shortcomings are addressed by SenSE due application examples within different jupyter notebooks.

# Acknowledgements

In memory of Alexander Löw (&#8224; 2 July 2017) who started this library.

[//]: # (The author also wishes to thank the reviewers and editors for their efforts and for their helpful comments to improve this paper and the software package.)

# References
