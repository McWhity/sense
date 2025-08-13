from dataclasses import dataclass

import numpy as np


@dataclass
class SurfaceScatter():
    """Major surface scatter class."""

    eps: complex | np.ndarray = None
    ks: float = None
    theta: float | np.ndarray = None
    kl: float = None
    mv: float | np.ndarray = None
    C_hh: float = None
    C_vv: float = None
    C_hv: float = None
    D_hh: float = None
    D_vv: float = None
    D_hv: float = None
