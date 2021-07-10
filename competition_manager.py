from competition_results import CompetitionResults
from jump_simulator import JumpSimulator
import random
import matplotlib.pyplot as plt
import numpy as np


class CompetitionManager:
    def __init__(self, hill, competition_data, jumpers):
        self.hill = hill
        self.rounds = int(competition_data['rounds'])
        self.jumpers = jumpers
        self.seed = int(competition_data['seed'])
        self.gate = int(competition_data['gate'])
        self.results = CompetitionResults(hill, competition_data['date'], jumpers)
        self.simulator = JumpSimulator(self.hill)
        self.jump_seed_gen = random.Random(self.seed)
        self.wind_init()

    def run_jump(self, jumper, debug=False):
        jump_seed = self.next_jump_seed()
        wind = self.get_wind(jump_seed)
        jump_res, flight_path = self.simulator.simulate_jump(
            jumper, wind, self.gate, jump_seed)
        if debug:
            self.render_jump(
                flight_path[0], flight_path[1], jump_res.distance, self.hill.profile)
        return jump_res

    def run_competition(self, debug=False):
        for round in range(self.rounds):
            for ind, jumper in enumerate(self.jumpers):
                x = self.run_jump(jumper, debug)
                self.results.add_jump_result(ind, x)
                # print(x)
            self.results.sort_results()

            # for x in self.results.ordered_results():
            #     print(x)

    def next_jump_seed(self):
        return self.jump_seed_gen.randint(0, 6574036)

    def wind_init(self):
        self.wind_gen = random.Random(self.seed)
        self.wind_base = -3 + 6 * self.wind_gen.random()
        self.wind_bias = self.wind_gen.random() * 2

    def get_wind(self, jump_seed):
        gen = random.Random(jump_seed)
        return gen.random() * self.wind_bias + self.wind_base
    
    def present_results(self):
        print('Ski Jumping Competition', self.hill.name, self.results.date)
        for res in self.results.ordered_results():
            athlete = res.athlete
            jumps = res.jump_results
            print(res.rank, athlete.name, athlete.country, res.total_points)
            for ind, jmp in enumerate(jumps):
                print(f'\t{ind+1}. {jmp}')
            

    def render_jump(self, fly_x, fly_y, dist, hill):
        plt.title(f'{dist} m')
        plt.plot(fly_x, fly_y, '--')
        x0 = np.linspace(hill.A[0], 0, 100)
        y0 = list(map(hill.inrun, x0))
        x1 = np.linspace(0, hill.U[0])
        y1 = list(map(hill.landing_area, x1))
        xd = [hill.P[0], hill.K[0], hill.L[0]]
        yd = [hill.P[1], hill.K[1], hill.L[1]]
        plt.plot(x0, y0)
        plt.plot(x1, y1)
        plt.plot(xd, yd, 'o')

        xt = []
        yt = []

        plt.axis('equal')
        plt.show()
