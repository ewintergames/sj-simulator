from hill_profile import HillProfile


def get_points_meter(k):
    if k < 25:
        return 4.8
    if k < 30:
        return 4.4
    if k < 35:
        return 4.0
    if k < 40:
        return 3.6
    if k < 50:
        return 3.2
    if k < 60:
        return 2.8
    if k < 70:
        return 2.4
    if k < 80:
        return 2.2
    if k < 100:
        return 2.0
    if k < 165:
        return 1.8
    return 1.2


def get_points_k(k):
    return 60 if k < 165 else 120


class Hill:
    def __init__(self, name, k, hs, gate_factor, gates_dist, headwind_factor, tailwind_factor, profile:HillProfile):
        self.name = name
        self.k = k
        self.hs = hs
        self.gate_factor = gate_factor
        self.gates_dist = gates_dist
        self.headwind_factor = headwind_factor
        self.tailwind_factor = tailwind_factor
        self.points_meter = get_points_meter(self.k)
        self.points_k = get_points_k(self.k)
        self.profile = profile

    def get_distance_points(self, distance):
        return (distance - self.k) * self.points_meter + self.points_k

    def get_gate_points(self, gates_diff):
        return -gates_diff * self.gates_dist * self.gate_factor * self.points_meter

    def get_wind_points(self, wind):
        wind_factor = self.headwind_factor if wind > 0 else self.tailwind_factor
        return -wind * wind_factor * self.points_meter
