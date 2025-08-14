"""Specification of canopies."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class OneLayer:
    """Define a homogeneous one layer canopy.

    Right now water_cloud and turbid_isotropic/turbid_rayleigh are implemented
    """

    canopy: str  # 'water_cloud', 'turbid_isotropic', or 'turbid_rayleigh'

    # Water cloud model params
    A_hh: Optional[float] = None
    B_hh: Optional[float] = None
    A_vv: Optional[float] = None
    B_vv: Optional[float] = None
    A_hv: Optional[float] = None
    B_hv: Optional[float] = None
    V1: Optional[float] = None
    V2: Optional[float] = None

    # Turbid isotropic / turbid rayleigh params
    ke_h: Optional[float] = None
    ke_v: Optional[float] = None
    ks_h: Optional[float] = None
    ks_v: Optional[float] = None
    d: Optional[float] = None

    def __post_init__(self):
        if self.canopy == 'water_cloud':
            required = ['A_hh', 'B_hh', 'A_vv', 'B_vv', 'A_hv', 'B_hv', 'V1', 'V2']
        elif self.canopy in ('turbid_isotropic', 'turbid_rayleigh'):
            required = ['ke_h', 'ke_v', 'ks_h', 'ks_v', 'd']
        else:
            raise ValueError(f"Unknown canopy model: {self.canopy}")

        for param in required:
            if getattr(self, param) is None:
                raise ValueError(f"{param} must be provided for canopy model '{self.canopy}'")
