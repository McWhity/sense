Usage
======

.. toctree::
    :maxdepth: 2

    ./notebooks/Oh04.ipynb
    ./notebooks/I2EM.ipynb
    ./notebooks/Dubois95_SSRT.ipynb
    ./notebooks/sm_retrieval.ipynb

Required input paramter
-------------------------

Surface RT models
~~~~~~~~~~~~~~~~~
Water Could Model (WCM - surface part)::
    c # empirical fitted soil parameter (calibration constant)
    d # empirical fitted soil parameter (indicates the sensitivity of soil moisture on the radar signal)
    sm # soil moisture [m³/m³]

Oh model from 1992 (Oh92)::
    theta # local incidence angle [radians]
    k # radar wave number
    s # surface roughness [m]
    f # frequency [GHz]    
    eps # dielectric constant of the soil

Oh model from 2004 (Oh04)::
    theta # local incidence angle [radians]
    k # radar wave number
    s # surface roughness [m]
    f # frequency [GHz]
    sm # soil moisture [m³/m³]

Dubois model from 1995 (Dubois95)::
    theta # local incidence angle [radians]
    k # radar wave number
    s # surface roughness [m]
    f # frequency [GHz]    
    eps # dielectric constant of the soil

Canopy RT models
~~~~~~~~~~~~~~~~~
Water Cloud Model (WCM - canopy part)::
    a # empirical fitted vegetation parameter
    b # empirical fitted vegetation parameter
    V1 # vegetation descriptor e.g., LAI/VWC
    V2 # vegetation descriptor e.g., LAI/VWC
    theta # local incidence angle [radians]

Single Scattering Radiative Transfer model (SSRT/S²RT)::
    omega # scattering albedo
    d # vegetation height [m]
    ke # extinction coefficient [m⁻¹]
    scattering assumption: Rayleigh or Turbid Isotropic


Dielectric mixing model (used to translate dielectric constant to soil moisture)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Simplistic approach with with temperature=23°C, bulk density=1.7 g/cm3::
    f # frequency [GHz]
    clay # clay content of the soil
    sand # sand content of the soil

Dobson et al. (1985)::
    f # frequency [GHz]
    clay # Clay content of the soil
    sand # Sand content of the soil
    bulk # bulk dry density of the soil [g/cm³]