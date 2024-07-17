import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)) + os.sep + "..")

from sense.scatterer import Scatterer, ScatIso, ScatRayleigh

class TestSingle(unittest.TestCase):
    def setUp(self):
        self.s_s_hh = 1.
        self.s_s_vv = 2.
        self.s_s_hv = 3.

    def test_scatterer_init(self):
        S = Scatterer(sigma_s_hh = self.s_s_hh, sigma_s_vv = self.s_s_vv, sigma_s_hv = self.s_s_hv)

    def test_iso(self):
        S = ScatIso(sigma_s_hh = self.s_s_hh, sigma_s_vv = self.s_s_hh, sigma_s_hv = self.s_s_hh)
        r = S.sigma_v_back()
        self.assertTrue(isinstance(r, dict))
        self.assertEqual(len(r), 3)

    def test_rayleigh(self):
        S = ScatRayleigh(sigma_s_hh = self.s_s_hh, sigma_s_vv = self.s_s_vv, sigma_s_hv = self.s_s_hv)
        r = S.sigma_v_back()
        self.assertTrue(isinstance(r, dict))
        self.assertEqual(len(r), 3)

    def test_rayleigh_v_back(self):

        Nv = 5.
        k_s = 2.
        
        sigma_s_pp = k_s

        S = ScatRayleigh(sigma_s_hh = sigma_s_pp, sigma_s_vv = sigma_s_pp, sigma_s_hv = sigma_s_pp)
        s_v = S.sigma_v_back()
        s_b = S.sigma_v_bist()

        for k in s_v.keys():
            if k == 'hv':
                pass
            else:
                self.assertEqual(s_v[k], s_b[k])
                self.assertEqual(s_v[k], 1.5*k_s)

    def test_iso_v_back(self):


        Nv = 7.
        k_s = 2.
        sigma_s_pp = k_s

        S = ScatIso(sigma_s_hh=sigma_s_pp, sigma_s_vv=sigma_s_pp, sigma_s_hv=sigma_s_pp)
        s_v = S.sigma_v_back()
        s_b = S.sigma_v_bist()

        for k in s_v.keys():
            self.assertEqual(s_v[k], s_b[k])
            self.assertEqual(s_v[k], k_s)

if __name__ == '__main__':
    unittest.main()
