
import matplotlib.pyplot as plt
import numpy as np

from .scatter import SurfaceScatter


class Oh04(SurfaceScatter):
    """Oh et al. (2004) empirical surface backscattering model.

    After Ulaby et al (2014), chapter 10.5
    """

    def __init__(self, mv, ks, theta):
        """Parameters.

        mv : float, ndarray
            volumetric soil moisture m3/m3
        ks : float
            product of wavenumber and rms height
            be aware that both need to have the same units
        theta : float, ndarray
            incidence angle [rad]
        """
        super(Oh04, self).__init__(mv=mv, ks=ks, theta=theta)

        # calculate p and q
        self._calc_p()
        self._calc_q()

        # calculate backascatter
        self.hv = self._calc_vh()
        # difference between hv and vh?
        self.vv = self.hv / self.q
        self.hh = self.hv / self.q * self.p

    def _calc_p(self):
        self.p = 1 - (2.*self.theta/np.pi)**(0.35*self.mv**(-0.65)) * np.exp(-0.4 * self.ks**1.4)

    def _calc_q(self):
        self.q = 0.095 * (0.13 + np.sin(1.5*self.theta))**1.4 * (1-np.exp(-1.3 * self.ks**0.9))

    def _calc_vh(self):
        a = 0.11 * self.mv**0.7 * np.cos(self.theta)**2.2
        b = 1 - np.exp(-0.32 * self.ks**1.8)
        return a*b

    def plot(self):
        f = plt.figure()
        ax = f.add_subplot(111)
        t = np.rad2deg(self.theta)
        ax.plot(t, 10.*np.log10(self.hh), color='blue', label='hh')
        ax.plot(t, 10.*np.log10(self.vv), color='red', label='vv')
        ax.plot(t, 10.*np.log10(self.hv), color='green', label='hv')
        ax.grid()
        #ax.set_ylim(-25.,0.)
        #ax.set_xlim(0.,70.)
        ax.legend()
        ax.set_xlabel('incidence angle [deg]')
        ax.set_ylabel('backscatter [dB]')





