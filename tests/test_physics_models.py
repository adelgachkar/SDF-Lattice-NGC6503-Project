"""Tests for the shared kernels used by the model comparison."""

import math
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sdf_lattice import physics as P


class ConstantsTests(unittest.TestCase):
    def test_a0_conversion(self):
        # 1 (km/s)^2/kpc == 3.2408e-14 m/s^2, so 1.2e-10 m/s^2 is ~3702.8
        self.assertAlmostEqual(P.A0_KPC, 3702.8, places=1)
        self.assertAlmostEqual(P.A0_KPC * 1e6 / P.KPC_TO_M, 1.2e-10, places=20)

    def test_g_units(self):
        # G in kpc (km/s)^2 / Msun, converted to m^3 kg^-1 s^-2, must agree with SI.
        g_si = 6.6743e-11
        converted = (P.G_KPC_KM2_MSUN * P.KPC_TO_M * 1e6) / 1.98892e30
        self.assertLess(abs(converted / g_si - 1.0), 5e-3)


class ZetaTests(unittest.TestCase):
    def test_limits_and_midpoint(self):
        self.assertAlmostEqual(P.zeta(P.DEFAULT_R0_KPC), 0.5, places=15)
        self.assertLess(P.zeta(0.0), 1e-3)
        self.assertGreater(P.zeta(10.0), 1 - 1e-9)

    def test_monotone(self):
        values = [P.zeta(r) for r in (0.1, 0.5, 1.0, 2.0, 4.0, 8.0)]
        self.assertTrue(all(a < b for a, b in zip(values, values[1:])))

    def test_invalid(self):
        with self.assertRaises(ValueError):
            P.zeta(-1.0)
        with self.assertRaises(ValueError):
            P.zeta(1.0, dr=0.0)


class SdfTests(unittest.TestCase):
    def test_asymptote_is_v_inf_without_overshoot(self):
        for v_bar in (10.0, 60.0, 116.0):
            self.assertAlmostEqual(P.sdf_velocity(5000.0, v_bar), P.DEFAULT_V_INF_KMS, places=9)
            self.assertLessEqual(P.sdf_velocity(5.0, v_bar), P.DEFAULT_V_INF_KMS + 1e-9)

    def test_core_matches_baryons(self):
        # zeta(0) is 3.3e-4, not 0, so the core sits a few hundredths above v_bar.
        core = P.sdf_velocity(1e-9, 35.8)
        self.assertGreater(core, 35.8)
        self.assertLess(core - 35.8, 0.1)


class NfwTests(unittest.TestCase):
    def test_inner_slope_is_half_in_velocity(self):
        # NFW mass rises as r^2 near the centre, so v_nfw^2 ~ r and v_nfw ~ sqrt(r).
        rho_s, r_s = 1e7, 10.0
        v1 = P.nfw_velocity_squared(1e-3, rho_s, r_s)
        v4 = P.nfw_velocity_squared(4e-3, rho_s, r_s)
        self.assertAlmostEqual(v4 / v1, 4.0, places=2)
        self.assertAlmostEqual(math.sqrt(v4 / v1), 2.0, places=2)

    def test_velocity_adds_in_quadrature(self):
        v = P.nfw_velocity(5.0, 50.0, 1e7, 10.0)
        expected = math.sqrt(50.0 ** 2 + P.nfw_velocity_squared(5.0, 1e7, 10.0))
        self.assertAlmostEqual(v, expected, places=12)
        self.assertGreater(v, 50.0)

    def test_validation(self):
        with self.assertRaises(ValueError):
            P.nfw_velocity_squared(1.0, -1.0, 10.0)
        with self.assertRaises(ValueError):
            P.nfw_velocity_squared(1.0, 1e7, 0.0)


class MondTests(unittest.TestCase):
    def test_deep_mond_limit(self):
        # v^4 = G M a0: at tiny g_bar, v^2 approaches sqrt(g_bar a0) * r.
        r, v_bar = 20.0, 1.0
        g_bar = v_bar ** 2 / r
        v = P.mond_velocity(r, v_bar)
        limit = math.sqrt(g_bar * P.A0_KPC) * r
        self.assertLess(abs(v ** 2 / limit - 1.0), 5e-3)

    def test_newtonian_limit(self):
        # nu -> 1 + 1/(2y) at large y, so the excess is ~a0/(2 g_bar).
        r, v_bar = 2.0, 1e4
        g_bar = v_bar ** 2 / r
        excess = P.mond_velocity(r, v_bar) / v_bar - 1.0
        self.assertLess(excess, 1e-4)
        self.assertGreater(excess, 0.0)
        self.assertAlmostEqual(excess, P.A0_KPC / (2 * g_bar), places=6)

    def test_interpolations_bracket(self):
        for r, v_bar in ((1.0, 50.0), (10.0, 50.0)):
            simple = P.mond_velocity(r, v_bar, interpolation="simple")
            standard = P.mond_velocity(r, v_bar, interpolation="standard")
            base = v_bar
            self.assertGreaterEqual(simple, standard)
            self.assertGreater(standard, base)

    def test_validation(self):
        with self.assertRaises(ValueError):
            P.mond_nu(0.0)
        with self.assertRaises(ValueError):
            P.mond_nu(1.0, interpolation="bogus")
        with self.assertRaises(ValueError):
            P.mond_velocity(1.0, 10.0, a0_kpc=-1.0)


class StatisticsTests(unittest.TestCase):
    def test_chi_squared_and_dof(self):
        chi, dof = P.chi_squared([1.0, 2.0], [0.0, 0.0], [1.0, 1.0], 1)
        self.assertAlmostEqual(chi, 5.0)
        self.assertEqual(dof, 1)

    def test_aic_bic(self):
        self.assertAlmostEqual(P.aic(10.0, 2), 14.0)
        self.assertAlmostEqual(P.bic(10.0, 2, 31), 10.0 + 2 * math.log(31), places=12)

    def test_chi_squared_validation(self):
        with self.assertRaises(ValueError):
            P.chi_squared([1.0], [1.0], [1.0], 1)  # dof = 0
        with self.assertRaises(ValueError):
            P.chi_squared([1.0], [1.0], [0.0], 0)


class DataTests(unittest.TestCase):
    def test_rotmod_parses(self):
        path = Path(__file__).resolve().parent.parent / "data" / "NGC6503_rotmod.dat"
        rows, distance = P.load_rotmod(path)
        self.assertEqual(len(rows), 31)
        self.assertAlmostEqual(distance, 6.26, places=9)
        self.assertAlmostEqual(rows[0]["r"], 0.76, places=9)
        self.assertAlmostEqual(rows[-1]["r"], 23.50, places=9)
        self.assertTrue(all(row["err"] > 0 for row in rows))


class SameConditionsTests(unittest.TestCase):
    """The comparison must fit every family to one table under one Upsilon and one p."""

    @classmethod
    def setUpClass(cls):
        path = Path(__file__).resolve().parent.parent / "data" / "NGC6503_rotmod.dat"
        cls.rows, _ = P.load_rotmod(path)
        cls.ups = 0.62
        cls.sdf = P.fit_sdf(cls.rows, cls.ups)
        cls.nfw = P.fit_nfw(cls.rows, cls.ups)
        cls.mond = P.fit_mond(cls.rows, cls.ups, "standard")
        cls.mond_free = P.fit_mond(cls.rows, cls.ups, "standard", free_a0=True)

    def test_chi2_nu_uses_n_minus_p_on_these_points(self):
        for fit, p in ((self.sdf, 1), (self.nfw, 2), (self.mond, 0), (self.mond_free, 1)):
            self.assertEqual(fit["n_parameters"], p)
            self.assertAlmostEqual(fit["chi2_nu"], fit["chi2"] / (31 - p), places=10)
            self.assertAlmostEqual(fit["aic"], fit["chi2"] + 2 * p, places=10)

    def test_rmse_is_the_unweighted_residual_rms(self):
        for fit, kind in ((self.sdf, "sdf"), (self.nfw, "nfw"), (self.mond, "mond_standard")):
            predicted = P._predict(self.rows, kind, fit)
            expected = math.sqrt(sum((row["v_obs"] - model) ** 2
                                      for row, model in zip(self.rows, predicted)) / len(self.rows))
            self.assertAlmostEqual(fit["rmse"], expected, places=9)
        # The adopted-parameter row reproduces the published 4.133 km/s.
        self.assertAlmostEqual(self.sdf["rmse"], 4.133, places=3)

    def test_one_upsilon_feeds_every_family(self):
        # The shared M/L must actually enter every family, not just SDF: shifting it
        # moves chi^2 for all three, in the same direction.
        higher = 0.80
        for kind, fitter in (("sdf", lambda u: P.fit_sdf(self.rows, u)),
                             ("nfw", lambda u: P.fit_nfw(self.rows, u)),
                             ("mond", lambda u: P.fit_mond(self.rows, u, "standard", free_a0=True))):
            baseline = P._chi2_for(self.rows, kind if kind != "mond" else "mond_standard",
                                   fitter(self.ups))
            shifted = P._chi2_for(self.rows, kind if kind != "mond" else "mond_standard",
                                  fitter(higher))
            self.assertGreater(abs(shifted - baseline), 1e-6, f"{kind} ignores Upsilon")
        # MOND with a0 fixed and Upsilon fixed is a zero-parameter prediction.
        self.assertEqual(self.mond["n_parameters"], 0)
        self.assertAlmostEqual(self.mond["aic"], self.mond["chi2"], places=12)

    def test_a_free_parameter_never_loses_to_a_fixed_one(self):
        self.assertLessEqual(self.mond_free["chi2"], self.mond["chi2"] + 1e-9)
        nfw_free = P.fit_nfw(self.rows, self.ups, True)
        self.assertLessEqual(nfw_free["chi2"], self.nfw["chi2"] + 1e-9)


if __name__ == "__main__":
    unittest.main()
