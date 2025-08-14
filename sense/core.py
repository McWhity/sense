
import matplotlib.pyplot as plt
import numpy as np


class Fresnel0:
    """Fresnel reflectivity at nadir (Ulaby, 2014, Eq. 10.36)."""

    def __init__(self, eps: complex):
        """Parameters.

        eps : complex
            Complex relative dielectric permittivity.
        """
        self.x = self._calc(eps)

    @staticmethod
    def _calc(eps: complex):
        return np.abs((1 - np.sqrt(eps)) / (1 + np.sqrt(eps))) ** 2

class Reflectivity:
    """Calculate reflectivity for H and V polarization."""

    def __init__(self, eps: complex, theta: float | np.ndarray):
        """Table 2.5 Ulaby (2014) assume specular surface.

        Parameters
        ----------
        eps : complex
            Relative dielectric permittivity.
        theta : float, ndarray
            Incidence angle [rad].
        """
        self.eps = eps
        self.theta = theta

        self.rho_v, self.rho_h = self._calc_reflection_coefficients()
        self.v = np.abs(self.rho_v) ** 2
        self.h = np.abs(self.rho_h) ** 2

    def _calc_reflection_coefficients(self):
        """Calculate reflection coefficients (Woodhouse, 2006, Eq. 5.54, 5.55)."""
        # OLD
        co = np.cos(self.theta)
        si2 = np.sin(self.theta) ** 2.
        rho_v = (self.eps * co - np.sqrt(self.eps - si2)) / \
                     (self.eps * co + np.sqrt(self.eps - si2))
        rho_h = (co - np.sqrt(self.eps - si2)) / \
                (co + np.sqrt(self.eps - si2))

        # srv = rho_v
        # srh = rho_h

        # # FROM PRISM1_FORWARDMODEL-1.m
        # n1 = np.sqrt(1.)
        # n2 = np.sqrt(self.eps)
        # costh2 = np.sqrt(1-(n1*np.sin(self.theta)/2.)**2)

        # rho_v = -(n2*np.cos(self.theta) - n1*costh2)/(n2*np.cos(self.theta) + n1*costh2)
        # rho_h = (n1*np.cos(self.theta) - n2*costh2)/(n1*np.cos(self.theta) + n2*costh2)

        # plt.plot(np.rad2deg(self.theta), rho_v-srv, label = 'v_diff')
        # plt.plot(np.rad2deg(self.theta), rho_h-srh, label = 'h_diff')
        # plt.legend()
        # # doesn't make much difference in results!

        return rho_v, rho_h

    def plot(self):
        fig, ax = plt.subplots()
        ax.plot(np.rad2deg(self.theta), self.v, color='red', linestyle='-', label='V')
        ax.plot(np.rad2deg(self.theta), self.h, color='blue', linestyle='--', label='H')
        ax.set_xlabel('Incidence angle [deg]')
        ax.set_ylabel('Reflectivity')
        ax.grid(True)
        ax.legend()
        plt.show()

