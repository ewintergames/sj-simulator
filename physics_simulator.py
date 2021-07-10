from hill_profile import HillProfile
import numpy as np


class PhysicsSimulator:
    gravity = np.array([0, -9.81])

    def __init__(self, hill:HillProfile):
        self.hill = hill
        self.aero_coeffs_fun = None

    def landed(self, pos):
        return pos[1] <= self.hill.landing_area(pos[0])

    def simulate_inrun(self, gate, inrun_coeff):
        start_point = self.hill.B + \
            (self.hill.A - self.hill.B) * (gate - 1) / self.hill.gates
        return (2 * 9.81 * start_point[1])**0.5 - inrun_coeff

    def simulate_flight(self, v0, takeoff, wind):
        pos = np.array([0.0, 0.0])
        vel = takeoff * np.array([np.sin(self.hill.alpha), np.cos(self.hill.alpha)]) + \
            v0 * np.array([np.cos(-self.hill.alpha), np.sin(-self.hill.alpha)])

        dt = 0.01

        fly_x = [0]
        fly_y = [0]
        while not self.landed(pos):
            angle = -np.rad2deg(np.arctan2(vel[1], vel[0]))
            tangent = vel / np.linalg.norm(vel)
            normal = np.array([-tangent[1], tangent[0]])
            lift, drag = self.aero_coeffs_fun(angle)
            # lift = self.get_ka(jumper['flight'], 50, angle)
            # drag = get_kw(jumper['flight'], 50, angle)
            aero_force = (lift * normal - drag * tangent) * \
                (np.linalg.norm(vel) + wind)**2

            vel += (self.gravity * 70/70 + aero_force) * dt
            pos += vel * dt
            nor = self.hill.get_normal(pos[0])
            tan = np.array([1, self.hill.landing_area(pos[0] + 0.5) -
                            self.hill.landing_area(pos[0] - 0.5)])
            tan /= np.linalg.norm(tan)
            nor = np.array([-tan[1], tan[0]])

            fly_x.append(pos[0])
            fly_y.append(pos[1])
        return (fly_x, fly_y, pos, np.dot(vel, nor))
