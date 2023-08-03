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
It implements different existing models for scattering and emission for different surfaces in a coherent framework
to simulate SAR backscattering coefficients as function of surface biogeophysical parameters.
In the microwave domain the surface and volume contribution of the total backscatter is usually estimated separately.
Within the SenSE framework different model combination of surface and volume scatting models can be easily brought together
and moreover analyzed. The analysis of the different model combination within one framework can be seen as
the biggest advantage of the developed SenSE package. Currently implemented surface models are:
Oh92, Oh04, Dubois95 and IEM and Water Cloud (surface part). Currently implemented canopy models are:
SSRT and WCM.
Additionally, dielectric mixing models of .... (different versions) is implemented as well.
Furthermore, utility functions for ..... are implemented as well 

check another word for implemented

# Statement of need
Over the last decades several different (empirical to physical based) RT models were developed, 
tested and further modified. 
But a easy usable framework combing the most common microwave RT models (simulating backscatter 
response of active microwave sensors) is missing.
Thus, every researcher has to code their own implementation from the original source.
This python framework shall serves as a first attempt to combine most common active microwave related RT
models in a modular way.
Thus, surface and volume scattering models can be easily ausgetauscht werden
Such a modular framework reveals an opportunity to easily plug and play with different RT model combinations.
Furthermore, die Anwendung wird erleichtert inbesondere für comparision analysis. 
In time the framework is expected to grow, thus including more and more RT models
(e.g., passive microwave domain) and sublimentary functions (e.g., more dielectric mixing models)

# Method

Include graphic
Auflistung von allen RT modellen

Surface-scattering RT models

Volume-scattering RT models

Dielectric mixing models for soils

Detailed information are given in RtD and the original source of each model

# Applications
The python framework was used within the EU sponsored MULTIPLY Project.
Furthermore, the RT models implementation in SenSE was an important asset for the analysis carried out in 
publications ........
Further, Zusammenarbeit with researcher in the field of VOD are already in planung.
Thus, SenSE will be further used and further extensions are to be expected. 


# Other available software scripts

## Ulaby and Long code library
Ulaby and Long wrote a extensive book about the fundamentals of microwave remote sensing.
They also provided a ton of matlab codes for demonstration purposes.
But, as the matlab codes are individual code snippets for different RT models, it is not easy to plug and play
with different RT model combinations.
Thus, one advantage of SenSE is a easier usability (jupyter notebooks etc)



# Acknowledgements

In memory of Alexander Löw (&#8224; 2. July 2017) who started this library.

[//]: # (The author also wishes to thank the reviewers and editors for their efforts and for their helpful comments to improve this paper and the software package.)

# References
