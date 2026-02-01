import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)) + os.sep + "..")

# from sense.surface import I2EM

# class Test_IEM(unittest.TestCase):
#     def setUp(self):
#         self.eps = 4.+0.j
#         self.theta = 0.5
#         self.f = 6.
#         self.s = 0.01
#         self.l = 0.1

#     def tearDown(self):
#         pass
    
#     def test_init(self):
#         model = I2EM(self.f, self.eps, self.s, self.l, self.theta, auto=False)
#         self.assertEqual(model.eps, self.eps)
#         self.assertEqual(model.ks, model.k*model.sig)
#         self.assertEqual(model.kl, model.k*model.l)

#     def test_scat(self):
#         model = I2EM(self.f, self.eps, self.s, self.l, self.theta, auto=False)

# if __name__ == '__main__':
#    unittest.main()
