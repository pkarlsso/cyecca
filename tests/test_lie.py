import unittest

from pathlib import Path
import cProfile
from pstats import Stats

import sympy

from cyecca import lie


class ProfiledTestCase(unittest.TestCase):
    def setUp(self):
        self.pr = cProfile.Profile()
        self.pr.enable()

    def tearDown(self) -> None:
        p = Stats(self.pr)
        p.strip_dirs()
        p.sort_stats("cumtime")
        profile_dir = Path(".profile")
        profile_dir.mkdir(exist_ok=True)
        p.dump_stats(profile_dir / self.id())


class Test_LieGroupRn(ProfiledTestCase):
    def test_ctor(self):
        v = ca.DM([1, 2, 3])
        self.assertTrue(ca.norm_2(G1.param - v) < EPS)
        self.assertEqual(G1.n_dim, 3)

    def test_bad_operations(self):
        G1 = LieGroupR(3, ca.DM([1, 2, 3]))
        G2 = LieGroupR(3, ca.DM([4, 5, 6]))
        s = ca.SX.sym("s")
        with self.assertRaises(TypeError):
            G1 + G2
        with self.assertRaises(TypeError):
            G1 - G2
        with self.assertRaises(TypeError):
            G1 @ G2
        with self.assertRaises(TypeError):
            s * G2

    def test_product(self):
        v1 = ca.DM([1, 2, 3])
        v2 = ca.DM([4, 5, 6])
        v3 = v1 + v2
        G1 = LieGroupR(3, ca.DM([1, 2, 3]))
        G2 = LieGroupR(3, ca.DM([4, 5, 6]))
        G3 = G1 * G2
        self.assertTrue(ca.norm_2(G3.param - v3) < EPS)

    def test_identity(self):
        G1 = LieGroupR(3, [1, 2, 3])


class Test_LieAlgebraR(ProfiledTestCase):
    def test_ctor(self):
        v = ca.DM([1, 2, 3])
        g1 = LieAlgebraR(3, v)
        self.assertTrue(ca.norm_2(g1.param - v) < EPS)
        self.assertEqual(g1.n_dim, 3)

    def test_bad_operations(self):
        pass

    def test_add(self):
        v1 = ca.DM([1, 2, 3])
        v2 = ca.DM([4, 5, 6])
        v3 = v1 + v2
        g1 = LieAlgebraR(3, ca.DM([1, 2, 3]))
        g2 = LieAlgebraR(3, ca.DM([4, 5, 6]))
        g3 = g1 + g2
        self.assertEqual(g3, LieAlgebraR(3, v3))


class Test_LieAlgebraSO2(ProfiledTestCase):
    def test_ctor(self):
        v = ca.DM([1])
        G1 = LieAlgebraSO2(1)

    def test_identity(self):
        e = LieGroupSO2.identity()
        G = LieGroupSO2(2)
        self.assertEqual(G, e * G)


class Test_LieGroupSO2(ProfiledTestCase):
    def test_ctor(self):
        v = ca.DM([1])
        G1 = LieGroupSO2(1)


class Test_LieGroupSO3(ProfiledTestCase):
    def test_ctor(self):
        v = ca.DM([1])
        G1 = LieGroupSO3Quat([1, 0, 0, 0])

    def test_identity(self):
        e = LieGroupSO3Quat.identity()
        G2 = LieGroupSO3Quat([0, 1, 0, 0])
        self.assertEqual(e * G2, G2)
        self.assertEqual(G2 * e, G2)
        self.assertEqual(G2, G2)

    def test_addition(self):
        g = LieAlgebraSO3([1, 2, 3])
        self.assertEqual(g + g, LieAlgebraSO3(2 * g.param))
        self.assertEqual(g - g, LieAlgebraSO3([0, 0, 0]))
        self.assertEqual(-g, LieAlgebraSO3([-1, -2, -3]))

    def test_exp_log(self):
        g = LieAlgebraSO3([1, 2, 3])
        self.assertEqual(g, LieGroupSO3Quat.exp(g).log())


if __name__ == "__main__":
    unittest.main()
