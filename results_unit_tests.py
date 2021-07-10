from jump_result import JumpResult
from result import Result
from hill import Hill
from jumper import Jumper
import unittest


class ResultsUnitTest(unittest.TestCase):
    def setUp(self):
        self.hill = Hill('Zakopane HS140', 125, 140, 4.2, 0.62, 6, 7.26, None)
        self.jmp1 = JumpResult(90.3, 136.5, 0, 0.18, [
                               18, 18.5, 18.5, 18, 18.5], self.hill)
        self.jmp2 = JumpResult(89.9, 134.5, -1, 0.20,
                               [18.5, 18.5, 19, 18.5, 18.5], self.hill)

    def test_jump_result1(self):
        jmp = self.jmp1
        self.assertAlmostEqual(jmp.total_points, 133.8, 3)
        self.assertAlmostEqual(jmp.distance_points, 80.7, 3)
        self.assertAlmostEqual(jmp.wind_points, -1.9, 3)
        self.assertAlmostEqual(jmp.gate_points, 0, 3)
        self.assertAlmostEqual(jmp.judges_total, 55, 3)

    def test_jump_result2(self):
        jmp = self.jmp2
        self.assertAlmostEqual(jmp.total_points, 135.1, 3)
        self.assertAlmostEqual(jmp.distance_points, 77.1, 3)
        self.assertAlmostEqual(jmp.wind_points, -2.2, 3)
        self.assertAlmostEqual(jmp.gate_points, 4.7, 3)
        self.assertAlmostEqual(jmp.judges_total, 55.5, 3)

    def test_result(self):
        rk = Jumper("Ryoyu Kobayashi", "JPN", 80, 85, 95, 98)
        u = Result(rk)
        u.add_jump(self.jmp1)
        u.add_jump(self.jmp2)
        self.assertAlmostEqual(u.total_points, 268.9, 3)


class HillUnitTest(unittest.TestCase):
    def test_normal_hill(self):
        normal_hill = Hill(None, 90, 100, 0, 0, 0, 0, None)
        self.assertEqual(normal_hill.points_k, 60)
        self.assertEqual(normal_hill.points_meter, 2)

    def test_large_hill(self):
        large_hill = Hill(None, 125, 140, 0, 0, 0, 0, None)
        self.assertEqual(large_hill.points_k, 60)
        self.assertEqual(large_hill.points_meter, 1.8)

    def test_flying_hill(self):
        flying_hill = Hill(None, 200, 240, 0, 0, 0, 0, None)
        self.assertEqual(flying_hill.points_k, 120)
        self.assertEqual(flying_hill.points_meter, 1.2)


if __name__ == '__main__':
    unittest.main()
