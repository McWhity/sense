"""Definition of scatter types."""

from dataclasses import dataclass

import numpy as np


@dataclass
class Scatterer:
    """Base class for scatterers.

    Parameters
    -----------
    sigma_s_hh : float
        Particle HH scattering cross section [m²].
    sigma_s_vv : float
        Particle VV scattering cross section [m²].
    sigma_s_hv : float
        Particle HV scattering cross section [m²].
    """

    sigma_s_hh: float | np.ndarray = None
    sigma_s_vv: float | np.ndarray = None
    sigma_s_hv: float | np.ndarray = None

    def __post_init__(self):
        if self.sigma_s_hh is None:
            raise ValueError("HH scattering cross section must be specified [m²]")
        if self.sigma_s_vv is None:
            raise ValueError("VV scattering cross section must be specified [m²]")
        if self.sigma_s_hv is None:
            raise ValueError("HV scattering cross section must be specified [m²]")

@dataclass
class ScatIso(Scatterer):
    """Isotropic scatterer definition (see Ulaby 2014, 11.2)."""

    def sigma_v_back(self):
        """Volume backscattering coefficient for isotropic case.

        This corresponds to the volume scattering coefficient ks.
        Note: This is NOT the scattering cross section of a single particle!

        Returns
        --------
        dict
            Backscattering coefficients for 'hh', 'vv', 'hv'.
        """
        return {
            "hh": self.sigma_s_hh,
            "vv": self.sigma_s_vv,
            "hv": self.sigma_s_hv,
        }

    def sigma_v_bist(self):
        """Bistatic volume backscatter (same as sigma_v_back (Eq. 11.19))."""
        return self.sigma_v_back()


@dataclass
class ScatRayleigh(Scatterer):
    """Rayleigh scatterer definition (see Ulaby 2014, 11.2)."""

    def sigma_v_back(self):
        """Volume backscattering coefficient for Rayleigh scatterers.

        Returns
        -------
        dict
            Backscattering coefficients for 'hh', 'vv', 'hv'.
            Note: 'hv' is undefined (np.nan).
        """
        return {
            "hh": 1.5 * self.sigma_s_hh,
            "vv": 1.5 * self.sigma_s_vv,
            "hv": np.nan,
        }

    def sigma_v_bist(self):
        """Bistatic volume backscatter (same as sigma_v_back (Eq. 11.22))."""
        return self.sigma_v_back()

