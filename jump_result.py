import numpy as np
from hill import Hill


class JumpResult:
    def __init__(self, speed, distance, gates_diff, wind, judges_points, hill: Hill):
        self.speed = np.round(speed, 1)
        self.distance = distance
        self.distance_points = hill.get_distance_points(distance)
        self.gates_diff = gates_diff
        self.gate_points = np.round(hill.get_gate_points(gates_diff), 1)
        self.wind = wind
        self.wind_points = np.round(hill.get_wind_points(wind), 1)
        self.judges_points = judges_points
        self.judges_total = self.calculate_judges_points()
        self.total_points = np.round(max(
            0, self.distance_points + self.judges_total + self.gate_points + self.wind_points), 1)

    def calculate_judges_points(self):
        mn = min(self.judges_points)
        mx = max(self.judges_points)
        return sum(self.judges_points) - mx - mn

    def get_total_points(self):
        return self.total_points

    def __str__(self):
        return f"{self.speed} km/h {self.distance} m ({self.gate_points}/{self.wind_points}) {self.judges_points} {self.total_points}"
