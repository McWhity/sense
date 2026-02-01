
from dataclasses import dataclass
from typing import Dict, List, Optional, Union

import numpy as np

from .core import Reflectivity
from .scatterer import ScatIso, ScatRayleigh
from .surface import I2EM, Dubois95, Oh04, Oh92, WaterCloudSurface
from .util import f2lam


@dataclass
class Model:
    """Basic class for scattering modelling."""
    theta: float

    def __post_init__(self):
        assert self.theta is not None, 'ERROR: no incidence angle was specified!'

    def sigma0(self, dB: bool = False, pol: Optional[List[str]] = None):
        """Calculate sigma.

        Parameters
        ----------
        dB : bool
            Return results in decibel.
        pol : list
            List with polarizations pq
            whereas p=receive, q=transmit
            p,g can be either H or V
        """
        self.dB = dB
        self.pol = pol or []
        #self._check_pol()

        sigma = self._sigma0()
        if self.dB:
            raise NotImplementedError('dB output for dictionaries is not supported.')
        return sigma

    def _sigma0(self):
        raise NotImplementedError('Routine should be implemented in child class!')

    def _check_pol(self):
        if not self.pol:
            raise AssertionError('ERROR: polarization needs to be specified')
        for k in self.pol:
            if k not in ['HH','VV','HV','VH']:
                raise AssertionError(f'Invalid polarization: {k}')

@dataclass
class RTModel(Model):
    """Radiative Transfer Models.
    
    SSRT Eq. 11.17 (Ulaby and Long 2014) or WCM (Attema and Ulaby 1978).

    Parameters
    ----------
    surface : Surface description
        Object describing the surface
    canopy : Canopy description
        Object describing the canopy
    models : dict
        Dictionary with configuration of scattering models
    """
    surface: object
    canopy: object
    models: Dict[str, str]
    freq: float
    coherent: bool = True  # default: use coherent simulations

    def __post_init__(self):
        super().__post_init__()
        self._check()
        self._sigma0()

    def _check(self):
        assert self.surface is not None
        assert self.canopy is not None
        assert self.models is not None
        assert self.freq is not None

        for key in ['surface', 'canopy']:
            assert key in self.models
        if self.models['surface'] != 'WaterCloud':
            assert self.freq == self.surface.f, "Frequency mismatch between model and surface"

    def _sigma0(self):
        """Calculate sigma0.

        based on Ulaby and Long 2014 (Eq. 11.17) or
        only ground and canopy contribution for water cloud model
        """
        self.G = Ground(
            self.surface,
            self.canopy,
            self.models['surface'],
            self.models['canopy'],
            theta=self.theta,
            freq=self.freq
        )
        self.s0g = self.G.sigma()              # ground contribution
        self.s0c = self.G.rt_c.sigma_c()       # canopy contribution

        if self.models['canopy'] in ['turbid_isotropic', 'turbid_rayleigh']:
            self.s0cgt = self.G.sigma_c_g(self.coherent)
            self.s0gcg = self.G.sigma_g_c_g()

        self.stot = {k: self._combine(k) for k in ['hh', 'vv', 'hv']}

    def _combine(self, k: str):
        """Combine previous calculated backscatter values.

        For SSRT (isotropic or rayleigh) or Water Cloud model
        """
        if any(val is None for val in [self.s0g.get(k), self.s0c.get(k)]):
            return None

        if self.models['canopy'] in ['turbid_isotropic', 'turbid_rayleigh']:
            return np.array(self.s0g[k] + self.s0c[k] + self.s0gcg[k] + self.s0cgt[k])
        elif self.models['canopy'] == 'water_cloud':
            return np.array(self.s0g[k] + self.s0c[k])
        else:
            raise AssertionError('Unknown canopy model!')













@dataclass
class Ground:
    """Calculate the (attenuated) ground contribution sigma_pq.

    p is receive and q is transmit polarization

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
    S: object
    C: object
    RT_s: str
    RT_c: str
    theta: float | np.ndarray
    freq: float

    def __post_init__(self):
        assert self.theta is not None, 'Theta/incidence angle needs to be provided'
        assert self.freq is not None, 'Frequency needs to be provided'
        self._check_models()
        self._set_models()
        
        if self.RT_c != 'water_cloud':
            self._calc_rho()

    def _check_models(self):
        valid_surfaces = ['Oh92', 'Oh04', 'Dubois95', 'WaterCloud']#, 'I2EM']
        valid_canopies = ['turbid_rayleigh', 'turbid_isotropic', 'water_cloud']
        assert self.RT_s in valid_surfaces, f'Invalid surface scattering model: {self.RT_s}'
        assert self.RT_c in valid_canopies, f'Invalid canopy model: {self.RT_c}'

    def _set_models(self):
        """Initialize surface and canopy RT models."""
        self.rt_s = self._init_surface_model()
        self.rt_c = self._init_canopy_model()

    def _init_surface_model(self):
        if self.RT_s == 'Oh92':
            return Oh92(self.S.eps, self.S.ks, self.theta)
        elif self.RT_s == 'Oh04':
            return Oh04(self.S.mv, self.S.ks, self.theta)
        elif self.RT_s == 'Dubois95':
            return Dubois95(
                self.S.eps, self.S.ks, self.theta, lam=f2lam(self.freq)
            )
        elif self.RT_s == 'I2EM':
            return I2EM(
                self.freq, self.S.eps, self.S.s, self.S.l, self.theta,
                xpol=False, auto=False
            )
        elif self.RT_s == 'WaterCloud':
            required_attrs = ['C_hh', 'C_vv', 'C_hv', 'D_hh', 'D_vv', 'D_hv']
            if not all(hasattr(self.S, attr) for attr in required_attrs):
                raise ValueError('Empirical parameters for WaterCloud model not specified!')
            return WaterCloudSurface(
                self.S.mv, self.theta,
                self.S.C_hh, self.S.C_vv, self.S.C_hv,
                self.S.D_hh, self.S.D_vv, self.S.D_hv
            )
        else:
            raise ValueError(f'Unknown surface scattering model: {self.RT_s}')

    def _init_canopy_model(self):
        if self.RT_c == 'turbid_isotropic':
            stype = 'iso'
        elif self.RT_c == 'turbid_rayleigh':
            stype = 'rayleigh'
        elif self.RT_c == 'water_cloud':
            return WaterCloudCanopy(
                A_hh=self.C.A_hh, B_hh=self.C.B_hh,
                A_vv=self.C.A_vv, B_vv=self.C.B_vv,
                A_hv=self.C.A_hv, B_hv=self.C.B_hv,
                V1=self.C.V1, V2=self.C.V2,
                theta=self.theta
            )
        else:
            raise ValueError(f'Invalid canopy scattering model: {self.RT_c}')

        return CanopyHomoRT(
            ke_h=self.C.ke_h, ke_v=self.C.ke_v,
            ks_h=self.C.ks_h, ks_v=self.C.ks_v,
            d=self.C.d, theta=self.theta,
            stype=stype
        )

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
        roughness = np.exp(-4 * np.cos(self.theta)**2 * (self.S.ks**2))
        self.rho_v = R.v * roughness
        self.rho_h = R.h * roughness

        # implementation in matlab code and book of Ulaby.
        # (Email response from Ulaby: Don't know why he didn't use the roughness correction.
        # He actually would use the roughness corrected version!!)
        # self.rho_v = R.v
        # self.rho_h = R.h

    def sigma_g_c_g(self):
        """Calculate ground canopy ground scattering coefficient (Ulaby 2014)."""
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
        """Backscattering coefficient (Eq. 11.4, p.463 Ulaby 2014)."""
        # canopy transmisivities
        t_h = self.rt_c.t_h
        t_v = self.rt_c.t_v

        # backscatter

        s_hh = self.rt_s.hh * t_h**2
        s_vv = self.rt_s.vv * t_v**2
        s_hv = None if getattr(self.rt_s, 'hv', None) is None or self.RT_s=='I2EM' else self.rt_s.hv * t_h * t_v


        s_hv = None
        if self.RT_s != 'I2EM' and self.rt_s.hv is not None:
            s_hv = self.rt_s.hv * t_v * t_h

        return {'vv' : s_vv, 'hh' : s_hh, 'hv' : s_hv}

@dataclass
class CanopyHomoRT:
    """Homogeneous canopy RT model.

    Assumes homogeneous vertical distribution of scatterers
    in that case the Lambert Beer law applies

    NOTE that this model is only for BACKSCATTERING GEOMETRY!

    Parameters
    ----------
    ke_h, ke_v : float
        volume extinction coefficient [Np/m]
    d : float
        height of canopy layer [m]
    theta : float, ndarray
        incidence angle [rad]
    """
    ke_h: float
    ke_v: float
    ks_h: float
    ks_v: float
    d: float
    theta: float | np.ndarray
    stype: str  # scatterer type: 'iso', 'rayleigh', 'cloud'

    def __post_init__(self):
        self._check()
        self.tau_h = self._tau(self.ke_h)
        self.tau_v = self._tau(self.ke_v)
        self.t_h = np.exp(-self.tau_h)
        self.t_v = np.exp(-self.tau_v)
        self._set_scat_type()
        self.sigma_vol_back = self._calc_back_volume()
        self.sigma_vol_bistatic = self._calc_sigma_bistatic()

    def _check(self):
        for attr in ['ke_h', 'ke_v', 'ks_h', 'ks_v', 'stype']:
            if getattr(self, attr) is None:
                raise ValueError(f"{attr} must be provided")
        if self.stype not in ['iso', 'rayleigh', 'cloud']:
            raise ValueError(f"Invalid scatterer type: {self.stype}")

    def _set_scat_type(self):
        """Set scatterer object based on type."""
        if self.stype == 'iso':
            self.SC = ScatIso(
                sigma_s_hh=self.ks_h,
                sigma_s_vv=self.ks_v,
                sigma_s_hv=self.ks_v
            ) #note that the cross pol scatt. coeff. is the same as the copol due to isotropic behavior
        elif self.stype == 'rayleigh':
            self.SC = ScatRayleigh(
                sigma_s_hh=self.ks_h,
                sigma_s_vv=self.ks_v,
                sigma_s_hv=self.ks_v
            ) # eq. 11.22
        elif self.stype == 'cloud':
            raise NotImplementedError("Cloud scatterer type not implemented yet")
            # here implemenatation of 11.5 then

    def _tau(self, k):
        """Compute optical depth (Eq. 11.3, Ulaby 2014)."""
        # assumption: extinction is isotropic
        return k * self.d / np.cos(self.theta)

    def _calc_back_volume(self):
        """Calculate the volume backscattering coefficient sigma_v.

        This is a function of the scatterer type chosen (e.g. isotropic,
        rayleigh, cloud model, ...)
        """
        return self.SC.sigma_v_back()

    def _calc_sigma_bistatic(self):
        """Calculate volume bistatic scattering coefficient of scatterer."""
        return self.SC.sigma_v_bist()

    def sigma_gcg(self, G_v, G_h):
        """Calculate ground-canopy-ground interactions (Eq. 11.16, Ulaby 2014).

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

        Eq. 11.10 + 11.16 as seen in 11.17, Ulaby 2014
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

@dataclass
class WaterCloudCanopy:
    """Water cloud model Attema and Ulaby (1978).

    Canopy part

    Parameters
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
    # Fitting parameters
    A_hh: float
    B_hh: float
    A_vv: float
    B_vv: float
    A_hv: float
    B_hv: float

    # Vegetation descriptors
    V1: float
    V2: float

    # Incidence angle [rad]
    theta: Union[float, np.ndarray]

    def __post_init__(self):
        # Compute optical depths
        self.tau_h = self._tau(self.B_hh)
        self.tau_v = self._tau(self.B_vv)
        self.tau_hv = self._tau(self.B_hv)

        # Compute square roots of optical depths
        self.t_h = np.sqrt(self.tau_h)
        self.t_v = np.sqrt(self.tau_v)
        self.t_hv = np.sqrt(self.tau_hv)

    def _tau(self, B: float) -> Union[float, np.ndarray]:
        """Compute the optical depth tau for a given B parameter."""
        return np.exp(-2 * B / np.cos(self.theta) * self.V2)

    def sigma_c(self) -> Dict[str, Union[float, np.ndarray]]:
        """Calculate canopy backscatter part."""
        s_hh = self.A_hh * self.V1 * np.cos(self.theta) * (1 - self._tau(self.B_hh))
        s_vv = self.A_vv * self.V1 * np.cos(self.theta) * (1 - self._tau(self.B_vv))
        s_hv = self.A_hv * self.V1 * np.cos(self.theta) * (1 - self._tau(self.B_hv))
        
        return {'hh': s_hh, 'vv': s_vv, 'hv': s_hv}
