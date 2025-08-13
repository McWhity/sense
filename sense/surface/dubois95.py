
import matplotlib.pyplot as plt
import numpy as np

from .scatter import SurfaceScatter


class Dubois95(SurfaceScatter):
    """Dubois95 model described in Ulaby (2014), Chapter 10.6."""

    def __init__(self, eps, ks, theta, lam: float):
        """Parameters.

        eps : complex, ndarray
            Relative dielectric permittivity
        ks : float
            Product of wavenumber and RMS height
        theta : float, ndarray
            Incidence angle [rad]
        lam : float
            Wavelength [m]
        """
        super().__init__(eps=eps, ks=ks, theta=theta)
        self.lam = lam
        assert self.lam is not None, "Wavelength `lam` must be provided."
        self.vv, self.hh = self._calc_sigma()
        self.hv = None

    def _calc_sigma(self):
        lam_cm = self.lam * 100  # convert from m to cm
        ks = self.ks # ks has no unity (s [cm or m], k [1/cm or 1/m])
        return self._vv(lam_cm, ks), self._hh(lam_cm, ks)

    def _hh(self, lam, ks):
        a = 10**-2.75 * (np.cos(self.theta) ** 1.5) / (np.sin(self.theta) ** 5)
        c = 10 ** (0.028 * np.real(self.eps) * np.tan(self.theta))
        d = (ks * np.sin(self.theta)) ** 1.4 * lam**0.7
        return a * c * d

    def _vv(self, lam, ks):
        """(Eq. 10.41b)."""
        b = 10**-2.35 * (np.cos(self.theta) ** 3) / (np.sin(self.theta) ** 3)
        c = 10 ** (0.046 * np.real(self.eps) * np.tan(self.theta))
        d = (ks * np.sin(self.theta)) ** 1.1 * lam**0.7
        return b * c * d

    def plot(self):
        """Plot backscatter vs incidence angle."""
        fig, ax = plt.subplots()
        t = np.rad2deg(self.theta)
        ax.plot(t, 10 * np.log10(self.hh), color='blue', label='hh')
        ax.plot(t, 10 * np.log10(self.vv), color='red', label='vv')
        # ax.plot(t, 10 * np.log10(self.hv), color='green', label='hv')
        ax.grid()
        ax.set_ylim(-35, -5)
        ax.set_xlim(30, 70)
        ax.legend()
        ax.set_xlabel('Incidence angle [deg]')
        ax.set_ylabel('Backscatter [dB]')
