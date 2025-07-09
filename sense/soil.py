
import numpy as np

from .dielectric import Dobson85
from .util import f2lam


class Soil(object):
    """Class specifying a soil."""
    def __init__(self, **kwargs):
        """Parameters.

        ----------
        surface: string
            name of used RT-model for surface contribution
        eps : complex
            relative permitivity, if this is not given, then mv needs to be given
        s : float
            surface rms height [m]
        mv : float
            volumetric soil moisture [m**3/m**3]; either eps or mv needs to be given
        f : float
            frequency [GHz]
        l : float
            optional: autocorrelation length
        acl : str
            identifier for shape of autocorrelation function
            G = Gaussian
            E = Exponential
        clay : float
            optional fractional clay content
        sand : float
            optional fraction sand content


        empirical soil parameters water cloud model missing!!!!
        """
        self.surface = kwargs.get('surface', None)
        self.eps = kwargs.get('eps', None)
        self.mv = kwargs.get('mv', None)
        self.f = kwargs.get('f', None)
        self.s = kwargs.get('s', None)
        self.l = kwargs.get('l', None)
        self.acl = kwargs.get('acl', None)
        self.clay = kwargs.get('clay', None)
        self.sand = kwargs.get('sand', None)
        self.debye = kwargs.get('debye', None)
        self.dc_model = kwargs.get('dc_model', 'Dobson85')
        self._check()
        if self.eps is not None:
            self._convert_eps2mv()
        if self.mv is not None:
            if self.surface != 'WaterCloud':
                self._convert_mv2eps()

        if self.surface != 'WaterCloud':
            # wavenumber
            self.k = 2.*np.pi / f2lam(self.f)  # note that wavenumber is in meter and NOT in cm!

            # roughness parameters
            self.ks = self.s*self.k
            if self.l is not None:
                self.kl = self.k*self.l
            else:
                self.kl = None

        # Empirical soil parameters for Water Cloud model
        self.C_hh = kwargs.get('C_hh', None)
        self.D_hh = kwargs.get('D_hh', None)
        self.C_vv = kwargs.get('C_vv', None)
        self.D_vv = kwargs.get('D_vv', None)
        self.C_hv = kwargs.get('C_hv', None)
        self.D_hv = kwargs.get('D_hv', None)
        self.V2 = kwargs.get('V2', None)

    def _convert_mv2eps(self):
        """Convert mv to eps using dielectric model."""
        if (self.clay is None) or (self.sand is None):
            self.eps = None
            print('WARNING: Permittivity can not be calculated due to missing soil texture!')
        if self.dc_model == 'Dobson85':
            DC = Dobson85(clay=self.clay, sand=self.sand, mv=self.mv, freq=self.f, debye=self.debye)
        else:
            assert False, 'Invalid DC model! ' + self.dc_model

        self.eps = DC.eps

    def _convert_eps2mv(self):
        """This routine converts soil moisture into dielectric properties and vice versa.

        future implementations will comprise e.g. the Dobson model
        and others ...
        """
        assert self.eps is not None, (
            'Currently conversion not implemented yet; you need to provide the DC directly!'
        )

    def _check(self):
        if self.acl is not None:
            assert self.acl in ['G','E'], 'Invalid form of autocorrelation function specified'
        if self.surface != 'WaterCloud':
            assert self.s is not None

        if self.eps is None:
            assert self.mv is not None, 'Either EPS or MV need to be given!'
        if self.mv is None:
            assert self.eps is not None, 'Either EPS or MV need to be given!'




