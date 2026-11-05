"""Rigorous deterministic tests for the velocity-tangent governor."""
import math
import unittest

from sdf_lattice.nodes.velocity_tangent_governor import VelocityTangentGovernorNode


class VelocityTangentGovernorTests(unittest.TestCase):
    def setUp(self):
        self.node = VelocityTangentGovernorNode("gov", {
            "speed_setpoint": 10.0, "speed_scale": 2.0, "gain": 1.0, "min_open": 0.1
        })

    def test_below_and_at_setpoint_fully_open(self):
        for velocity in (0.0, 10.0, -10.0, 9.5):
            out = self.node.compute({"tangential_velocity": velocity, "drive_pressure": 7.0})
            self.assertEqual(out["valve_fraction"], 1.0)
            self.assertEqual(out["regulated_pressure"], 7.0)
            self.assertEqual(out["feedback_pressure"], 0.0)

    def test_overspeed_is_negative_feedback_and_matches_equation(self):
        out = self.node.compute({"tangential_velocity": 12.0, "drive_pressure": 8.0})
        expected_opening = 0.1 + 0.9 / (1 + ((12 - 10) / 2) ** 2)
        self.assertAlmostEqual(out["valve_fraction"], expected_opening)
        self.assertAlmostEqual(out["regulated_pressure"], 8 * expected_opening)
        self.assertLess(out["feedback_pressure"], 0.0)
        self.assertLess(out["regulated_pressure"], 8.0)

    def test_feedback_is_monotonic_with_speed_and_never_amplifies(self):
        vals = [self.node.compute({"tangential_velocity": v, "drive_pressure": 3})["valve_fraction"]
                for v in (10, 11, 12, 20, 100)]
        self.assertEqual(vals[0], 1.0)
        self.assertTrue(all(a >= b for a, b in zip(vals, vals[1:])))
        self.assertTrue(all(0.1 <= x <= 1.0 for x in vals))

    def test_sign_invariance_and_collapse_pressure_bypass(self):
        pos = self.node.compute({"tangential_velocity": 14, "drive_pressure": 5})
        neg = self.node.compute({"tangential_velocity": -14, "drive_pressure": 5})
        self.assertEqual(pos, neg)
        collapse = self.node.compute({"tangential_velocity": 100, "drive_pressure": -4})
        self.assertEqual(collapse["regulated_pressure"], -4.0)
        self.assertEqual(collapse["feedback_pressure"], 0.0)

    def test_zero_and_signed_speed_and_default_drive(self):
        out = self.node.compute({"tangential_velocity": -12})
        self.assertEqual(out["speed"], 12.0)
        self.assertEqual(out["regulated_pressure"], 0.0)

    def test_parameter_and_input_validation(self):
        invalid = [
            ({"speed_setpoint": -1}, ValueError),
            ({"speed_scale": 0}, ValueError),
            ({"gain": -1}, ValueError),
            ({"min_open": 1.1}, ValueError),
            ({"gain": float("nan")}, ValueError),
        ]
        for params, exc in invalid:
            with self.subTest(params=params), self.assertRaises(exc):
                VelocityTangentGovernorNode("bad", params)
        for inputs in ({}, {"tangential_velocity": True},
                       {"tangential_velocity": float("inf")},
                       {"tangential_velocity": 1, "drive_pressure": float("nan")}):
            with self.subTest(inputs=inputs), self.assertRaises(ValueError):
                self.node.compute(inputs)
        with self.assertRaises(TypeError):
            self.node.compute(None)

    def test_gain_zero_is_open_and_minimum_open_clamps(self):
        open_node = VelocityTangentGovernorNode("open", {"gain": 0})
        self.assertEqual(open_node.compute({"tangential_velocity": 1e6, "drive_pressure": 2})["valve_fraction"], 1.0)
        shut = VelocityTangentGovernorNode("shut", {"speed_setpoint": 0, "speed_scale": 1, "gain": 1e6, "min_open": 0.2})
        result = shut.compute({"tangential_velocity": 1e6, "drive_pressure": 2})
        self.assertGreaterEqual(result["valve_fraction"], 0.2)
        self.assertLessEqual(result["valve_fraction"], 1.0)


if __name__ == "__main__":
    unittest.main()
