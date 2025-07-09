
import numpy as np

from .core import Reflectivity
from .scatterer import ScatIso, ScatRayleigh
from .surface import I2EM, Dubois95, Oh04, Oh92, WaterCloudSurface
from .util import f2lam


class Model(object):
    """Basic class for scattering modelling."""
    
    def __init__(self, **kwargs):
        self.theta = kwargs.get('theta', None)

        self._check1()

    def _check1(self):
        assert self.theta is not None, 'ERROR: no incidence angle was specified!'

    def sigma0(self, **kwargs):
        """Calculate sigma.

        Parameters
        ----------
        dB : bool
            return results in decibel
        pol : list
            list with polarizations pq
            whereas p=receive, q=transmit
            p,g can be either H or V
        """
        self.dB = kwargs.get('dB', False)
        self.pol = kwargs.get('pol', [])
        self._check_pol()

        if self.dB:
            assert False, 'Not supported for dictionaries yet!'
            return 10.*np.log10(self._sigma0())
        else:
            return self._sigma0()

    def _sigma0(self, **kwargs):
        assert False, 'routine should be implemented in child class!'

    def _check_pol(self):
        if len(self.pol) == 0:
            assert 'ERROR: polarization needs to be specified'
        for k in self.pol:
            if k not in ['HH','VV','HV','VH']:
                assert False, 'Invalid polarization: ' + k

class RTModel(Model):
    """Radiative Transfer Models."""

    def __init__(self, **kwargs):
        """SSRT Eq. 11.17 (Ulaby and Long (2014)) or WCM (Attema and Ulaby, 1978).

        Parameters
        ----------
        surface : Surface description
            object describing the surface
        canopy : Canopy description
            object describing the canopy
        models : dict
            dictionary with configuration of scattering models
        """
        super(RTModel, self).__init__(**kwargs)
        self.surface = kwargs.get('surface', None)
        self.canopy = kwargs.get('canopy', None)
        self.models = kwargs.get('models', None)
        self.freq = kwargs.get('freq', None)
        self.coherent = kwargs.get('coherent', True)  # use coherent simulations as default

        self._check()

    def _check(self):
        assert self.surface is not None
        assert self.canopy is not None
        assert self.models is not None
        assert self.freq is not None

        for k in ['surface', 'canopy']:
            assert k in self.models.keys()  # check that all models have been specified
        if self.models['surface'] != 'WaterCloud':
            assert self.freq == self.surface.f, "Different frequencies in model and soil definition"
            # check that frequencies are the same!

    def _sigma0(self):
        """Basic calculation of Sigma0 based on Eq. 11.17 in Ulaby and Long (2014).

        or only ground and canopy contribution for water cloud model
        """
        # ground backscatter = attenuated surface
        self.G = Ground(
            self.surface,
            self.canopy,
            self.models['surface'],
            self.models['canopy'],
            theta=self.theta,
            freq=self.freq
        )
        self.s0g = self.G.sigma()  # returns dictionary with different components

        # canopy contribution
        self.s0c = self.G.rt_c.sigma_c()   # returns a dictionary
        if (
            self.models['canopy'] == 'turbid_isotropic'
            or self.models['canopy'] == 'turbid_rayleigh'
        ):
            # total canopy ground contribution
            self.s0cgt = self.G.sigma_c_g(self.coherent)

            # ground-canopy-ground interaction
            self.s0gcg = self.G.sigma_g_c_g()

        # combine backscatter values
        self.stot = {}
        for k in ['hh', 'vv', 'hv']:
            self.stot.update({k : self._combine(k)})


    def _combine(self, k):
        """Combine previous calculated backscatter values.

        For SSRT (isotropic or rayleigh) or Water Cloud model
        """
        if self.s0g[k] is None:
            return None
        if self.s0c[k] is None:
            return None
        # return np.nansum(np.array([self.s0g[k], self.s0c[k], self.s0gcg[k], self.s0cgt[k]]))
        if (
            self.models['canopy'] == 'turbid_isotropic'
            or self.models['canopy'] == 'turbid_rayleigh'
        ):
            return np.array(self.s0g[k] + self.s0c[k] + self.s0gcg[k] + self.s0cgt[k])
        elif (self.models['canopy'] == 'water_cloud'):
            return np.array(self.s0g[k]+self.s0c[k])
        else:
            assert False, 'unknown canopy model!'


class Ground(object):
    """Calculate the (attenuated) ground contribution sigma_pq.

    p is receive and q is transmit polarization
    """
    def __init__(self, S, C, RT_s, RT_c, theta=None, freq=None):
        """Calculate the attenuated ground contribution to the scattering.

        Parameters
        ----------
        S : object
            descibing the surface properties
        C : object
            describing the canopy properties
        RT_s : str
            key describing the surface scattering model
        RT_c : str
            key specifying the canopy scattering model
        theta : float/array
            incidence angle [rad]
        freq : float
            frequency[GHz]
        """
        self.S = S
        self.C = C
        self.theta = theta
        assert self.theta is not None, 'Theta/incidence angle needs to be provided'
        self._check(RT_s, RT_c)
        self.freq = freq
        assert self.freq is not None, 'Frequency needs to be provided'
        self._set_models(RT_s, RT_c)
        if self.S.surface != 'WaterCloud':
            self._calc_rho()
        self.RT_s = RT_s

    def _check(self, RT_s, RT_c):
        valid_surface = ['Oh92', 'Oh04', 'Dubois95', 'WaterCloud', 'I2EM']
        valid_canopy = ['turbid_rayleigh', 'turbid_isotropic', 'water_cloud']
        assert RT_s in valid_surface, 'ERROR: invalid surface scattering model was chosen!'
        assert RT_c in valid_canopy, 'ERROR: invalid canopy model: ' + RT_c

    def _set_models(self, RT_s, RT_c):
        # set surface model
        if RT_s == 'Oh92':
            self.rt_s = Oh92(self.S.eps, self.S.ks, self.theta)
        elif RT_s == 'Oh04':
            self.rt_s = Oh04(self.S.mv, self.S.ks, self.theta)
        elif RT_s == 'Dubois95':
            self.rt_s = Dubois95(
                self.S.eps,
                self.S.ks,
                self.theta,
                lam=f2lam(self.freq)
            )
        elif RT_s == 'I2EM':
            # assert False, 'Implementation not completed'
            self.rt_s = I2EM(
                self.freq,
                self.S.eps,
                self.S.s,
                self.S.l,
                self.theta,
                xpol=False,
                auto=False
            )
        elif RT_s == 'WaterCloud':
            if (
                getattr(self.S, 'C_hh', None) is None or
                getattr(self.S, 'D_hh', None) is None or
                getattr(self.S, 'C_vv', None) is None or
                getattr(self.S, 'D_vv', None) is None or
                getattr(self.S, 'C_hv', None) is None or
                getattr(self.S, 'D_hv', None) is None
            ):
                assert False, 'Empirical surface parameters for Water Cloud model not specified!'
            else:
                self.rt_s = WaterCloudSurface(
                    self.S.mv,
                    self.theta,
                    self.S.C_hh,
                    self.S.C_vv,
                    self.S.C_hv,
                    self.S.D_hh,
                    self.S.D_vv,
                    self.S.D_hv
                )
        else:
            assert False, 'Unknown surface scattering model'


        # set canopy models
        if RT_c == 'turbid_isotropic':  # turbid media (homogenous vegetation)
            self.rt_c = CanopyHomoRT(
                ke_h=self.C.ke_h,
                ke_v=self.C.ke_v,
                ks_h=self.C.ks_h,
                ks_v=self.C.ks_v,
                d=self.C.d,
                theta=self.theta,
                stype='iso'
            )
        elif RT_c == 'turbid_rayleigh':
            self.rt_c = CanopyHomoRT(
                ke_h=self.C.ke_h,
                ke_v=self.C.ke_v,
                ks_h=self.C.ks_h,
                ks_v=self.C.ks_v,
                d=self.C.d,
                theta=self.theta,
                stype='rayleigh'
            )
        elif RT_c == 'water_cloud':
            self.rt_c = WaterCloudCanopy(
                A_hh=self.C.A_hh,
                B_hh=self.C.B_hh,
                A_vv=self.C.A_vv,
                B_vv=self.C.B_vv,
                A_hv=self.C.A_hv,
                B_hv=self.C.B_hv,
                V1=self.C.V1,
                V2=self.C.V2,
                theta=self.theta
            )
        else:
            assert False, 'Invalid canopy scattering model: ' + RT_c

    def _calc_rho(self):
        """Calculate coherent p-polarized reflectivity.

        Ref: Eq. 11.11 (Ulaby, 2014)

        Note that the specular reflectivity is corrected by a roughness term
        if ks>0.2

        however, a sensitivity analysis showed that even for ks==0.2
        deviations can be up to 15% for typical incidence angles
        Only in case that ks << 0.1, the correction can be neglected.
        We therefore always use the roughness correction factor!

        TODO: unclear so far how this relates to surface (soil) scattering models
        """
        R = Reflectivity(self.S.eps, self.theta)
        self.rho_v = R.v * np.exp(-4.*np.cos(self.theta)**2.*(self.S.ks**2.))
        self.rho_h = R.h * np.exp(-4.*np.cos(self.theta)**2.*(self.S.ks**2.))

        # implementation in matlab code and book of Ulaby.
        # (Email response from Ulaby: Don't know why he didn't use the roughness correction.
        # He actually would use the roughness corrected version!!)
        # self.rho_v = R.v
        # self.rho_h = R.h



    def sigma_g_c_g(self):
        """Calculate ground canopy ground scattering coefficient  Ulaby (2014)."""
        s_vv = (
            self.rt_c.sigma_vol_back['vv']
            * np.cos(self.theta)
            * self.rho_v
            * self.rho_v
            * (self.rt_c.t_v * self.rt_c.t_v - self.rt_c.t_v ** 4.)
            / (self.C.ke_v + self.C.ke_v)
        )
        s_hh = (
            self.rt_c.sigma_vol_back['hh']
            * np.cos(self.theta)
            * self.rho_h
            * self.rho_h
            * (self.rt_c.t_h * self.rt_c.t_h - self.rt_c.t_h ** 4.)
            / (self.C.ke_h + self.C.ke_h)
        )
        s_hv = (
            self.rt_c.sigma_vol_back['hv']
            * np.cos(self.theta)
            * self.rho_h
            * self.rho_v
            * (self.rt_c.t_h * self.rt_c.t_v - self.rt_c.t_h ** 2. * self.rt_c.t_v ** 2.)
            / (self.C.ke_h + self.C.ke_v)
        )


        return {'vv' : s_vv, 'hh' : s_hh, 'hv' : s_hv}


    def sigma_c_g(self, coherent=None):
        """Calculate canopy ground scattering coefficient.

        This is based on Eq. 11.17 (last term) in Ulaby (2014)
        and 11.14 in Ulaby (2014)

        for co-pol, coherent addition can be made as an option

        Parameters
        ----------
        coherent : bool
            do coherent calculation for co-pol calculations
        """
        assert coherent is not None, (
            'ERROR: please specify explicity if coherent calculations should be made.'
        )
        n = 2.0 if coherent else 1.0

        s_vv = (
            n * self.rt_c.sigma_vol_bistatic['vv'] * self.C.d *
            (self.rho_v + self.rho_v) * self.rt_c.t_v * self.rt_c.t_v
        )
        s_hh = (
            n * self.rt_c.sigma_vol_bistatic['hh'] * self.C.d *
            (self.rho_h + self.rho_h) * self.rt_c.t_h * self.rt_c.t_h
        )
        s_hv = (
            1.0 * self.rt_c.sigma_vol_bistatic['hv'] * self.C.d *
            (self.rho_v + self.rho_h) * self.rt_c.t_h * self.rt_c.t_v
        )


        return {'vv' : s_vv, 'hh' : s_hh, 'hv' : s_hv}



    def sigma(self):
        """Calculate the backscattering coefficient Eq. 11.4, p.463 Ulaby (2014)."""
        # canopy transmisivities
        t_h = self.rt_c.t_h
        t_v = self.rt_c.t_v

        # backscatter
        s_hh = self.rt_s.hh*t_h*t_h
        s_vv = self.rt_s.vv*t_v*t_v

        if self.RT_s == 'I2EM':
            s_hv = None
            # s_hv = self.rt_s.hv*t_v*t_h
        elif self.rt_s.hv is None:
            s_hv = None
        else:
            s_hv = self.rt_s.hv*t_v*t_h

        return {'vv' : s_vv, 'hh' : s_hh, 'hv' : s_hv}


class CanopyHomoRT(object):
    """homogeneous canopy RT model.

    Assumes homogeneous vertical distribution of scatterers
    in that case the Lambert Beer law applies

    NOTE that this model is only for BACKSCATTERING GEOMETRY!
    """
    def __init__(self, **kwargs):
        """Parameters.

        ----------
        ke_h, ke_v : float
            volume extinction coefficient [Np/m]
        d : float
            height of canopy layer [m]
        theta : float, ndarray
            incidence angle [rad]
        """
        self.ke_h = kwargs.get('ke_h', None)
        self.ke_v = kwargs.get('ke_v', None)
        self.ks_h = kwargs.get('ks_h', None)
        self.ks_v = kwargs.get('ks_v', None)
        self.theta = kwargs.get('theta', None)
        self.d = kwargs.get('d', None)
        #self.Nv = kwargs.get('Nv', 1.)
        self.stype = kwargs.get('stype', None)  # scatterer type

        self._check()

        self.tau_h = self._tau(self.ke_h)
        self.tau_v = self._tau(self.ke_v)

        self.t_h = np.exp(-self.tau_h)
        self.t_v = np.exp(-self.tau_v)
        # pdb.set_trace()
        self._set_scat_type()
        self.sigma_vol_back = self._calc_back_volume()
        self.sigma_vol_bistatic = self._calc_sigma_bistatic()

    def _check(self):
        assert self.stype is not None

        assert self.ke_h is not None
        assert self.ke_v is not None
        assert self.ks_h is not None
        assert self.ks_v is not None

        # assert self.ke_h.min() >=0.
        # assert self.ke_v.min() >=0.
        # assert self.ks_h.min() >=0.
        # assert self.ks_v.min() >=0.

        # assert self.ks_h <= self.ke_h
        # assert self.ks_v <= self.ke_v

    def _set_scat_type(self):
        """Set scatterer type."""
        if self.stype == 'iso':
            self.SC = ScatIso(
                sigma_s_hh=self.ks_h,
                sigma_s_vv=self.ks_v,
                sigma_s_hv=self.ks_v
            )#note that the cross pol scatt. coeff. is the same as the copol due to isotropic behavior
        elif self.stype == 'rayleigh':
            self.SC = ScatRayleigh(
                sigma_s_hh=self.ks_h,
                sigma_s_vv=self.ks_v,
                sigma_s_hv=self.ks_v
            )  # eq. 11.22
        elif self.stype == 'cloud':
            assert False  # here implemenatation of 11.5 then
        else:
            assert False, 'Invalid scatterer type specified: ' + self.stype

    def _calc_back_volume(self):
        """Calculate the volume backscattering coefficient sigma_v.

        This is a function of the scatterer type chosen (e.g. isotropic,
        rayleigh, cloud model, ...)
        """
        return self.SC.sigma_v_back()

    def _calc_sigma_bistatic(self):
        """Calculate volume bistatic scattering coefficient of scatterer."""
        return self.SC.sigma_v_bist()

    def _tau(self, k):
        """Eq. 11.3, Ulaby(2014)."""
        # assumption: extinction is isotropic
        return k*self.d/np.cos(self.theta)

    def sigma_gcg(self, G_v, G_h):
        """Calculate ground-canopy-ground interactions Eq. 11.16, Ulaby(2014).

        Parameters
        ----------
        G_v : float
            v-polarized coherent Fresnel reflectivity under rough conditions
            see eq. 11.11 for explanations. As this depends on the
            surface model used, these should be provided here explicitely
        G_h : float
            same as above, but for h-polarization.
        """
        return (
            G_v * G_h
            * (self.t_h * self.t_v - self.t_h ** 2. * self.t_v ** 2.)
            * (self.sigma_vol * np.cos(self.theta))
            / (self.ke_h + self.ke_v)
        )

    def sigma_c(self):
        """Calculate canopy volume contribution only.

        Eq. 11.10 + 11.16 as seen in 11.17, Ulaby (2014)
        """
        s_hh = (
            (1. - self.t_h * self.t_h)
            * (self.sigma_vol_back['hh'] * np.cos(self.theta))
            / (self.ke_h + self.ke_h)
        )
        s_vv = (
            (1. - self.t_v * self.t_v)
            * (self.sigma_vol_back['vv'] * np.cos(self.theta))
            / (self.ke_v + self.ke_v)
        )
        s_hv = (
            (1. - self.t_h * self.t_v)
            * (self.sigma_vol_back['hv'] * np.cos(self.theta))
            / (self.ke_h + self.ke_v)
        )

        # this seems o.k. here
#        a=self.sigma_vol_back['hh']
#        b=1.5*self.ks_h
#        print a,b,a-b, a/b, self.ks_h

        return {'hh' : s_hh, 'vv' : s_vv, 'hv' : s_hv}

# 502-503

class WaterCloudCanopy(object):
    """Water cloud model Attema and Ulaby (1978).

    Canopy part
    """
    def __init__(self, **kwargs):
        """Parameters.

        ----------
        A, B : float
            fitting parameters
        V1: float
            vegetation descriptor
        V2: float
            vegetation descriptor
        theta : float, ndarray
            incidence angle [rad]
        """
        self.A_hh = kwargs.get('A_hh', None)
        self.B_hh = kwargs.get('B_hh', None)
        self.A_vv = kwargs.get('A_vv', None)
        self.B_vv = kwargs.get('B_vv', None)
        self.A_hv = kwargs.get('A_hv', None)
        self.B_hv = kwargs.get('B_hv', None)
        self.V1 = kwargs.get('V1', None)
        self.V2 = kwargs.get('V2', None)
        self.theta = kwargs.get('theta', None)
        self.tau_h = self._tau(self.B_hh)
        self.tau_v = self._tau(self.B_vv)
        self.tau_hv = self._tau(self.B_hv)
        self.t_h = np.sqrt(self.tau_h)
        self.t_v = np.sqrt(self.tau_v)
        self.t_hv = np.sqrt(self.tau_hv)

    def _check(self):
        assert self.A_hh is not None
        assert self.B_hh is not None
        assert self.A_vv is not None
        assert self.B_vv is not None
        assert self.A_hv is not None
        assert self.B_hv is not None
        assert self.V1 is not None
        assert self.V2 is not None
        assert self.theta is not None

    def sigma_c(self):
        """Calculate canopy backscatter part."""
        s_hh =  self.A_hh * self.V1 * np.cos(self.theta) * (1 - self._tau(self.B_hh))
        s_vv = self.A_vv * self.V1 * np.cos(self.theta) * (1 - self._tau(self.B_vv))
        s_hv =  self.A_hv * self.V1 * np.cos(self.theta) * (1 - self._tau(self.B_hv))

        return {'hh' : s_hh, 'vv' : s_vv, 'hv' : s_hv}

    def _tau(self, B):
        return np.exp(-2 * B / np.cos(self.theta) * self.V2)

