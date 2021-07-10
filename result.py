from hill import Hill
from jumper import Jumper
from jump_result import JumpResult
import numpy as np


class Result:
    def __init__(self, jumper):
        self.athlete = jumper
        self.total_points = 0
        self.rank = 1
        self.jump_results = []

    def add_jump(self, jump_result):
        self.jump_results.append(jump_result)
        self.total_points += jump_result.get_total_points()
        self.total_points = np.round(self.total_points, 1)

    def __cmp__(self, other):
        return self.total_points - other.total_points
    
    def __lt__(self, other):
        return self.total_points < other.total_points

    def __str__(self):
        return f"{self.athlete} / {', '.join(map(str, self.jump_results))} / {self.total_points}"


if __name__ == '__main__':
    zako = Hill(125, 140, 4.2, 0.62, 6, 7.26)
    ks = Jumper("Kamil Stoch", "POL", 80, 85, 95, 98)
    rk = Jumper("Ryoyu Kobayashi", "JPN", 80, 85, 95, 98)
    heg = Jumper("Halvor Egner Granerud", "NOR", 80, 85, 95, 98)
    me = Jumper("Markus Eisenbichler", "GER", 80, 85, 95, 98)
    u = Result(rk)
    u.add_jump(JumpResult(90.3, 136.5, 0, 0.18, [
               18, 18.5, 18.5, 18, 18.5], zako))
    u.add_jump(JumpResult(89.9, 134.5, -1, 0.20,
                          [18.5, 18.5, 19, 18.5, 18.5], zako))
    print(u.jump_results[0], u.jump_results[0].distance_points, u.jump_results[0].wind_points, u.jump_results[0].gate_points)
    print(u.jump_results[1], u.jump_results[1].distance_points, u.jump_results[1].wind_points, u.jump_results[1].gate_points)
    print(u)
