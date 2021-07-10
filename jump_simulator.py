from hill import Hill
from numpy.linalg.linalg import norm
from jumper import Jumper
from jump_result import JumpResult
from physics_simulator import PhysicsSimulator

import numpy as np
import random


angles = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20,
          22, 24, 26, 28, 30, 32, 34, 36, 38, 40, 42, 44]
kw_pts = [[0.00185, 0.00204, 0.00223, 0.00243, 0.00261, 0.00281, 0.00301, 0.00319,
           0.00338, 0.00355, 0.00372, 0.00388, 0.00403, 0.00418, 0.00432, 0.00447,
           0.00462, 0.00479, 0.00502, 0.00537, 0.00614, 0.00691, 0.00767],
          [0.00232, 0.00245, 0.00258, 0.00272, 0.00285, 0.00298, 0.00311, 0.00325,
           0.00337, 0.00350, 0.00362, 0.00374, 0.00386, 0.00398, 0.00410, 0.00422,
           0.00436, 0.00453, 0.00474, 0.00504, 0.00553, 0.00602, 0.00651],
          [0.00261, 0.00271, 0.00282, 0.00293, 0.00304, 0.00315, 0.00326, 0.00337,
           0.00347, 0.00357, 0.00367, 0.00376, 0.00386, 0.00396, 0.00407, 0.00419,
           0.00432, 0.00449, 0.00471, 0.00503, 0.00555, 0.00606, 0.00658]]

ka_pts = [[0.00093, 0.00139, 0.00185, 0.00231, 0.00275, 0.00316, 0.00354, 0.00390,
           0.00424, 0.00455, 0.00484, 0.00511, 0.00534, 0.00555, 0.00574, 0.00591,
           0.00605, 0.00617, 0.00628, 0.00638, 0.00655, 0.00672, 0.00689],
          [0.00116, 0.00180, 0.00244, 0.00308, 0.00365, 0.00396, 0.00424, 0.00450,
           0.00472, 0.00492, 0.00508, 0.00522, 0.00534, 0.00543, 0.00550, 0.00555,
           0.00560, 0.00565, 0.00571, 0.00582, 0.00606, 0.00629, 0.00652],
          [0.00130, 0.00177, 0.00224, 0.00270, 0.00316, 0.00350, 0.00382, 0.00411,
           0.00436, 0.00459, 0.00479, 0.00496, 0.00510, 0.00521, 0.00531, 0.00538,
           0.00545, 0.00551, 0.00558, 0.00569, 0.00590, 0.00611, 0.00632]]

kw = [np.poly1d(np.polyfit(angles, kw_pt, 4)) for kw_pt in kw_pts]
ka = [np.poly1d(np.polyfit(angles, ka_pt, 4)) for ka_pt in ka_pts]


def get_aerodynamic_data(stat, max_stat, table, angle):
    half_max_stat = max_stat / 2
    if stat <= max_stat / 2:
        return table[2](angle) * (half_max_stat - stat) / half_max_stat + table[1](angle) * stat / half_max_stat
    return table[1](angle) * (max_stat - stat) / half_max_stat + table[0](angle) * (stat - half_max_stat) / half_max_stat


def get_kw(stat, max_stat, angle):
    return get_aerodynamic_data(stat, max_stat, kw, angle)


def get_ka(stat, max_stat, angle):
    return get_aerodynamic_data(stat, max_stat, ka, angle)


class JumpSimulator:
    def __init__(self, hill: Hill):
        self.hill = hill
        self.physics_sim = PhysicsSimulator(self.hill.profile)
        self.physics_sim.aero_coeffs_fun = self.get_aero_coeffs

    def simulate_jump(self, jumper: Jumper, wind, gate, jump_seed):
        self.jumper = jumper
        self.wind = wind
        self.gate = gate
        self.jump_seed = jump_seed

        inrun_vel = self.physics_sim.simulate_inrun(gate, jumper.get_inrun_coeff())
        inrun_speed_kmh = np.linalg.norm(inrun_vel) * 3.6
        takeoff = jumper.get_takeoff_speed()
        fly_x, fly_y, pos, normal_vel_land = self.physics_sim.simulate_flight(
            inrun_vel, takeoff, wind)
        distance = self.hill.profile.get_distance(pos[0])
        judges_points = self.get_judges_points(jump_seed, normal_vel_land)
        # print(normal_vel_land)
        return (JumpResult(inrun_speed_kmh, distance, 0, wind, judges_points, self.hill), (fly_x, fly_y))

    def get_aero_coeffs(self, angle):
        stat = self.jumper.get_flight_coeffs()
        return (get_ka(stat, 100, angle), get_kw(stat, 100, angle))

    def get_judges_points(self, jump_seed, normal_speed):
        normal_speed = -normal_speed
        stat = self.jumper.get_style()
        telemark = 4.2 + stat / 100
        two_legs = 5.6 + stat / 300
        touch = 6.4 + stat / 200
        if normal_speed <= telemark:
            base_score = 19
        elif normal_speed <= two_legs:
            base_score = 16.5
        elif normal_speed <= touch:
            base_score = 12.5
        else:
            base_score = 9.

        base_score *= 2

        random.seed(jump_seed)
        bias = 3 #int(np.round((40 - base_score) / 10))
        lower_bound = max(0, base_score - bias)
        upper_bound = min(40, base_score + bias)
        scores = [random.randint(
            lower_bound, upper_bound) / 2 for _ in range(5)]
        return scores
