
import matplotlib.pyplot as plt
import numpy as np

from ..core import Fresnel0, Reflectivity
from .scatter import SurfaceScatter


class Oh92(SurfaceScatter):
    """Oh et al. (1992) empirical surface backscattering model.

    Reference:
        Ulaby et al. (2014), Chapter 10.5
    """

    def __init__(self, eps, ks, theta):
        """Parameters.

        eps : complex, ndarray
            Relative dielectric permittivity.
        ks : float
            Product of wavenumber and RMS height (same units).
        theta : float, ndarray
            Incidence angle [rad].
        """
        super().__init__(eps=eps, ks=ks, theta=theta)

        # Fresnel reflectivities
        self.G0 = Fresnel0(self.eps)  # Nadir Fresnel reflectivity
        self.G = Reflectivity(self.eps, self.theta)

        # Model parameters
        self.p = self._calc_p()
        self.q = self._calc_q()

        # Backscatter coefficients
        self._vv0 = self._calc_vv()
        self.vv = self._vv0
        self.hh = self.p * self._vv0
        self.hv = self.q * self._vv0

    def _calc_p(self):
        a = 1.0 / (3.0 * self.G0.x)
        return (1.0 - (2.0 * self.theta / np.pi) ** a * np.exp(-self.ks)) ** 2

    def _calc_q(self):
        return 0.23 * np.sqrt(self.G0.x) * (1.0 - np.exp(-self.ks))

    def _calc_vv(self):
        a = 0.7 * (1.0 - np.exp(-0.65 * self.ks ** 1.8))
        b = np.cos(self.theta) ** 3 * (self.G.v + self.G.h) / np.sqrt(self.p)
        return a * b

    def plot(self):
        fig, ax = plt.subplots()
        t = np.rad2deg(self.theta)
        ax.plot(t, 10 * np.log10(self.hh), color='blue', label='hh')
        ax.plot(t, 10 * np.log10(self.vv), color='red', label='vv')
        ax.plot(t, 10 * np.log10(self.hv), color='green', label='hv')
        ax.grid(True)
        ax.set_ylim(-25.0, 0.0)
        ax.set_xlim(0.0, 70.0)
        ax.legend()
        ax.set_xlabel('Incidence angle [deg]')
        ax.set_ylabel('Backscatter coefficient [dB m²/m²]')
        plt.show()
