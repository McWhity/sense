
from dataclasses import dataclass

import numpy as np

from .epsmodel import EpsModel


@dataclass
class Dobson85(EpsModel):
    """Dielectric mixing model for soils After Dobson et al. (1985).

    Coding after Ulaby (2014), Chapter 4
    """
    debye: bool = False
    single_debye: bool = False

    def __post_init__(self):
        super().__post_init__()
        self._init_model_parameters()
        self.ew = self._calc_ew()
        self.eps = self._calc_eps()

    def _calc_ew(self):
        """Calculate dielectric permittivity of free water.

        Using either the Debye model or a more simplistic approach.
        """
        if self.debye:
            # single Debye dielectric model for pure water. Eqs. 4.14
            # or Debye model with conductivity term for e2. Eqs. 4.67
            return self._debye()
        else:
            # default setting
            # simplistic approach using Eq. 4.69
            return self._simple_ew()

    def _simple_ew(self):
        """Simplistic approach with T=23°C, bulk density = 1.7 g/cm3.

        Eq. 4.69. (Ulaby et al., 2014)
        """
        f0 = 18.64   # relaxation frequency [GHz]
        hlp = self.freq/f0
        e1 = 4.9 + (74.1)/(1.+hlp**2.)
        e2 =(74.1*hlp)/(1.+hlp**2.) + 6.46 * self.sigma/self.freq
        return e1 + 1.j * e2

    def _debye(self):
        """Debye model.

        1) single Debye dielectric model for pure water. Eqs. 4.14
        2) (default) Debye model with conductivity term for e2. Eqs. 4.67.
        """
        f = self.freq *10**9
        ew_inf = 4.9 # determined by Lane and Saxton 1952 (E.4.15)
        ew_0 = (
            88.045
            - 0.4147 * self.temp
            + 6.295e-4 * self.temp**2
            + 1.075e-5 * self.temp**3
        )
        tau_w = (
            (1.1109e-10
            - 3.824e-12 * self.temp
            + 6.938e-14 * self.temp**2
            - 5.096e-16 * self.temp**3)
            / (2. * np.pi)
        )
        e1 = ew_inf +(ew_0-ew_inf)/(1 + (2*np.pi*f*tau_w)**2)

        if self.single_debye:
            # single Debye dielectric model for pure water. Eqs. 4.14
            e2 = 2*np.pi*f*tau_w * (ew_0-ew_inf) / (1 + (2*np.pi*f*tau_w)**2)
        else:
            # Debye model with conductivity term for e2. Eqs. 4.67
            e2 = (
                2 * np.pi * f * tau_w * (ew_0 - ew_inf)
                / (1 + (2 * np.pi * f * tau_w)**2)
                + (2.65 - self.bulk) / 2.65 / self.mv
                * self.sigma / (2 * np.pi * 8.854e-12 * f)
            )
        return e1 + 1.j *e2

    def _init_model_parameters(self):
        """Model parameters, eq. 4.68, Ulaby (2014)."""
        self.alpha = 0.65
        self.beta1 = 1.27-0.519*self.sand - 0.152*self.clay
        self.beta2 = 2.06 - 0.928*self.sand -0.255*self.clay
        self.sigma = -1.645 + 1.939*self.bulk - 2.256*self.sand + 1.594*self.clay

    def _calc_eps(self):
        """Calculate dielectric permittivity. Eq. 4.66 (Ulaby et al., 2014)."""
        e1 = (1. + 0.66 * self.bulk
            + self.mv**self.beta1 * np.real(self.ew)**self.alpha - self.mv
        ) ** (1. / self.alpha)
        e2 = np.imag(self.ew)*self.mv**self.beta2
        return e1 + 1.j*e2

