from dataclasses import dataclass, field
from typing import Optional

import numpy as np

from .dielectric import Dobson85
from .util import f2lam


@dataclass
class Soil:
    """Class specifying a soil.

    Parameters
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
    C_hh : float
        empirical parameter (Water Cloud Model)
    D_hh : float
        empirical parameter (Water Cloud Model)
    C_vv : float
            empirical parameter (Water Cloud Model)
    D_vv : float
        empirical parameter (Water Cloud Model)
    C_hv : float
        empirical parameter (Water Cloud Model)
    D_hv : float
        empirical parameter (Water Cloud Model)
    V2 : float
        parameter specifying the vegetation (Water Cloud Model)
    """

    # Soil parameters for different models
    surface: Optional[str] = None
    eps: Optional[complex] = None
    mv: Optional[float] = None
    f: Optional[float] = None
    s: Optional[float] = None
    l: Optional[float] = None
    acl: Optional[str] = None
    clay: Optional[float] = None
    sand: Optional[float] = None
    debye: Optional[float] = None
    dc_model: str = "Dobson85"

    # Soil parameters for Water Cloud model
    C_hh: Optional[float] = None
    D_hh: Optional[float] = None
    C_vv: Optional[float] = None
    D_vv: Optional[float] = None
    C_hv: Optional[float] = None
    D_hv: Optional[float] = None
    V2: Optional[float] = None

    # Computed fields (not set by user)
    k: Optional[float] = field(init=False, default=None)
    ks: Optional[float] = field(init=False, default=None)
    kl: Optional[float] = field(init=False, default=None)



    def __post_init__(self):
        """Run checks and compute dependent parameters after initialization."""
        self._check()

        # Convert between eps and mv if needed
        if self.eps is not None:
            self._convert_eps2mv()
        if self.mv is not None and self.surface != 'WaterCloud':
            self._convert_mv2eps()

        # Roughness parameters (only if not WaterCloud)
        if self.surface != 'WaterCloud':
            self.k = 2.0 * np.pi / f2lam(self.f)  # Wavenumber in m⁻¹ (not cm⁻¹)
            self.ks = self.s * self.k
            self.kl = self.k * self.l if self.l is not None else None

    def _convert_mv2eps(self):
        """Convert mv to eps using dielectric model."""
        if (self.clay is None) or (self.sand is None):
            self.eps = None
            print("WARNING: Permittivity cannot be calculated due to missing soil texture!")
            return

        if self.dc_model == 'Dobson85':
            DC = Dobson85(
                clay=self.clay,
                sand=self.sand,
                mv=self.mv,
                freq=self.f,
                debye=self.debye
            )
        else:
            raise ValueError(f"Invalid DC model! {self.dc_model}")

        self.eps = DC.eps

    def _convert_eps2mv(self):
        """This routine converts soil moisture into dielectric properties and vice versa.

        future implementations will comprise e.g. the Dobson model
        and others ...
        """
        assert self.eps is not None, (
            "Currently conversion not implemented yet; "
            "you need to provide the DC directly!"
        )

    def _check(self):
        """Basic parameter validation."""
        if self.acl is not None:
            assert self.acl in ['G', 'E'], (
                "Invalid form of autocorrelation function specified"
            )

        if self.surface != 'WaterCloud':
            assert self.s is not None, "Surface RMS height (s) is required"

        if self.eps is None:
            assert self.mv is not None, "Either eps or mv needs to be given!"
        if self.mv is None:
            assert self.eps is not None, "Either eps or mv needs to be given!"
