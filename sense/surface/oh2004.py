
import matplotlib.pyplot as plt
import numpy as np

from .scatter import SurfaceScatter


class Oh04(SurfaceScatter):
    """Oh et al. (2004) empirical surface backscattering model.

    Reference:
        Ulaby et al. (2014), Chapter 10.5
    """

    def __init__(self, mv, ks, theta):
        """Parameters.

        mv : float, ndarray
            Volumetric soil moisture [m³/m³].
        ks : float
            Product of wavenumber and RMS height (same units).
        theta : float, ndarray
            Incidence angle [rad].
        """
        super().__init__(mv=mv, ks=ks, theta=theta)

        # Model parameters
        self.p = self._calc_p()
        self.q = self._calc_q()

        # Backscatter coefficients
        self.hv = self._calc_vh()
        self.vv = self.hv / self.q
        self.hh = self.hv / self.q * self.p

    def _calc_p(self):
        return (
            1.0
            - (2.0 * self.theta / np.pi) ** (0.35 * self.mv ** -0.65)
            * np.exp(-0.4 * self.ks ** 1.4)
        )

    def _calc_q(self):
        return (
            0.095
            * (0.13 + np.sin(1.5 * self.theta)) ** 1.4
            * (1.0 - np.exp(-1.3 * self.ks ** 0.9))
        )

    def _calc_vh(self):
        a = 0.11 * self.mv ** 0.7 * np.cos(self.theta) ** 2.2
        b = 1.0 - np.exp(-0.32 * self.ks ** 1.8)
        return a * b

    def plot(self):
        fig, ax = plt.subplots()
        t = np.rad2deg(self.theta)
        ax.plot(t, 10.0 * np.log10(self.hh), color='blue', label='hh')
        ax.plot(t, 10.0 * np.log10(self.vv), color='red', label='vv')
        ax.plot(t, 10.0 * np.log10(self.hv), color='green', label='hv')
        ax.grid(True)
        ax.legend()
        ax.set_xlabel('Incidence angle [deg]')
        ax.set_ylabel('Backscatter [dB]')
        plt.show()



