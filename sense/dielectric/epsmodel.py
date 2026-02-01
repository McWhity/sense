
from dataclasses import dataclass
from typing import Optional

import numpy as np


@dataclass
class EpsModel:
    """Generic model for dielectric mixing models."""

    clay: Optional[float] = None # clay content as fractional volume
    sand: Optional[float] = None # sand content as fractional volume
    mv: Optional[float] = None # volumetric soil moisture content [cm**3/cm**3] = [g/cm**3]
    freq: Optional[float | np.ndarray] = None # frequency [GHz]
    bulk: float = 1.65 # bulk density [g/cm**3]; default: 1.65
    temp: float = 23.0 # temperature [°C]; default 23°C

    def __post_init__(self):
        """Run validation checks after dataclass is initialized."""
        assert self.clay is not None, "Clay needs to be provided!"
        assert 0.0 <= self.clay <= 1.0, "Clay must be between 0 and 1"
        assert self.sand is not None, "Sand needs to be provided!"
        assert 0.0 <= self.sand <= 1.0, "Sand must be between 0 and 1"
        assert self.mv is not None, "Volumetric soil moisture must be provided"
        assert self.freq is not None, "Frequency must be provided"

        if isinstance(self.freq, np.ndarray):
            assert np.all(self.freq > 0.0), "All frequency values must be > 0"
        else:
            assert self.freq > 0.0, "Frequency must be > 0"
