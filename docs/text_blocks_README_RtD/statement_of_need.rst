Over the last several decades, various (empirical to physically based) RT models in the active microwave domain have been developed, tested, and further modified.
However, an easy-to-use framework combining the most common microwave RT models (simulating backscatter responses of active microwave sensors) is lacking.
Thus, every researcher must produce their own code implementation from the original source.
This Python framework aims to serve as a first attempt to combine the most common active microwave-related RT models in a modular way.
As a result, surface and volume scattering models can be easily exchanged with one another.
Such a modular framework provides an opportunity to easily plug and play with different RT model combinations for various research questions and use cases.
SenSE facilitates the application of RT models, especially for comparative analysis.
Over time, the framework is expected to grow, incorporating more RT models (e.g., passive microwave domain) and supplementary functions (e.g., more dielectric mixing models).

While SenSE is a theoretical framework, it is designed to be compatible with data from a wide range of active microwave platforms, including both space-borne missions—such as Sentinel-1 (C-band), ALOS-2 PALSAR-2 (L-band), and TerraSAR-X (X-band)—and various air-borne SAR sensors.
To utilize data from these platforms within the framework, the primary requirement is the provision of sensor-specific parameters, namely the incidence angle (θ), the radar frequency or wavelength, and the polarization state (e.g., VV, VH, HH).
Additionally, since the RT models within SenSE typically operate on calibrated backscatter coefficients, input data must be pre-processed to provide sigma nought backscatter values.