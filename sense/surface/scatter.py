
class SurfaceScatter(object):
    """Major surface scatter class."""
    def __init__(
        self,
        eps=None,
        ks=None,
        theta=None,
        kl=None,
        mv=None,
        C_hh=None,
        C_vv=None,
        C_hv=None,
        D_hh=None,
        D_vv=None,
        D_hv=None,
        **kwargs
    ):
        self.eps = eps
        self.ks = ks
        self.theta = theta
        self.kl = kl

        self.mv = mv
        self.C_hh = C_hh
        self.C_vv = C_vv
        self.D_hh = D_hh
        self.D_vv = D_vv
        self.C_hv = C_hv
        self.D_hv = D_hv

        self._check()

    def _check(self):
        pass
        # assert isinstance(self.eps, complex)

