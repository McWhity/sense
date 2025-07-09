
import matplotlib.pyplot as plt
import numpy as np

from .scatter import SurfaceScatter


class WaterCloudSurface(SurfaceScatter):
    """Attema and Ulaby (1978): Vegetation modeled as a water cloud.

    Only surface part.
    """

    def __init__(self, mv, theta, C_hh, C_vv, C_hv, D_hh, D_vv, D_hv):
        """Parameters.

        mv : float, ndarray
            soil moisture [m³/m³]
        theta : float, ndarray
            incidence angle [rad]
        C : float
            empirical parameter
        D : float
            empirical parameter
        """
        super(WaterCloudSurface, self).__init__(
            mv=mv,
            theta=theta,
            C_hh=C_hh,
            C_vv=C_vv,
            C_hv=C_hv,
            D_hh=D_hh,
            D_vv=D_vv,
            D_hv=D_hv
        )

        # calculate surface component
        # if self.C_vv and self.D_vv:
        self.vv = self._calc_vv()
        # else:
            # self.vv = None

        # if self.C_hh and self.D_hh:
        self.hh = self._calc_hh()
        # else:
            # self.hh = None

        # if self.C_hv and self.D_hv:
        self.hv = self._calc_hv()
        # else:
            # self.hv = None

    def _calc_vv(self):
        return 10.**(((self.C_vv + self.D_vv * self.mv))/10)

    def _calc_hh(self):
        return 10.**(((self.C_hh + self.D_hh * self.mv))/10)

    def _calc_hv(self):
        return 10.**(((self.C_hv + self.D_hv * self.mv))/10)

    def plot(self):
        f = plt.figure()
        ax = f.add_subplott(111)
        t = np.rad2deg(self.theta)
        ax.plot(t, 10*np.log10(self.hh), color='blue', label='hh')
        ax.plot(t, 10*np.log10(self.vv), color='red', label='vv')
        ax.plot(t, 10*np.log10(self.hv), color='green', label='hv')
        ax.grid()
        ax.set_ylim(-25.,0.)
        ax.set_xlim(0.,70.)
        ax.legend()
        ax.set_xlabel('incidence angle [deg]')
        ax.set_ylabel('backscatter [dB]')

