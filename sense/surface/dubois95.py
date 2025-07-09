
import matplotlib.pyplot as plt
import numpy as np

from .scatter import SurfaceScatter


class Dubois95(SurfaceScatter):
    """Dubois95 model described in Ulaby (2014), Chapter 10.6."""

    def __init__(self, eps, ks, theta, lam=None):
        """Parameters.

        ----------
        eps : complex
            relative dielectric permitivity
        ks : float
            product of wavenumber and rms height
            be aware that both need to have the same units
        theta : float
            incidence angle in [rad]
        lam : float
            wavelength [m]
        """
        super(Dubois95, self).__init__(eps, ks, theta)
        self.lam = lam
        assert self.lam is not None
        self.vv, self.hh = self._calc_sigma()
        self.hv = None

    def _calc_sigma(self):
        lam = self.lam*100.  # from m in cm
        ks = self.ks  # ks has no unity (s [cm or m], k [1/cm or 1/m])
        return self._vv(lam, ks), self._hh(lam, ks)

    def _hh(self, lam, ks):
        """Lam : float; wavelength in cm."""
        a = (10.**-2.75)*(np.cos(self.theta)**1.5)/(np.sin(self.theta)**5.)
        c = 10.**(0.028*np.real(self.eps)*np.tan(self.theta))
        d = ((ks*np.sin(self.theta))**1.4)*lam**0.7

        return a*c*d

    def _vv(self, lam, ks):
        """Eq. 10.41b."""
        b = 10.**(-2.35)*((np.cos(self.theta)**3.) / (np.sin(self.theta)**3.))
        c = 10.**(0.046*np.real(self.eps)*np.tan(self.theta))
        d = (ks*np.sin(self.theta))**1.1*lam**0.7

        return b*c*d

    def plot(self):
        """Plotting helper."""
        f = plt.figure()
        ax = f.add_subplot(111)
        t = np.rad2deg(self.theta)
        ax.plot(t, 10.*np.log10(self.hh), color='blue', label='hh')
        ax.plot(t, 10.*np.log10(self.vv), color='red', label='vv')
        # ax.plot(t, 10.*np.log10(self.hv), color='green', label='hv')
        ax.grid()
        ax.set_ylim(-35.,-5.)
        ax.set_xlim(30.,70.)
        ax.legend()
        ax.set_xlabel('incidence angle [deg]')
        ax.set_ylabel('backscatter [dB]')
