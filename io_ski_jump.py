from jumper import Jumper
from hill_profile import HillProfile
from hill import Hill
from competition_manager import CompetitionManager
import csv
import matplotlib.pyplot as plt
import numpy as np
import argparse


class IOSkiJump:
    def __init__(self, jumpers_path, hills_path, competitions_path):
        self.jumpers_data = self.read_csv_data(jumpers_path)
        self.hills_data = self.read_csv_data(hills_path)
        self.competitions_data = self.read_csv_data(competitions_path)

    def read_csv_data(self, file_path):
        data = []
        with open(file_path, 'r+') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                data.append(row)
        return data

    def get_hill_data_by_name(self, hill_name):
        for x in self.hills_data:
            if x['name'] == hill_name:
                return x

    def get_hill_from_hill_data(self, hd):
        hill_profile = HillProfile(int(hd['type']), int(hd['gates']), float(hd['w']), float(hd['h']),
                                   float(hd['n']), float(hd['alpha']), float(
                                       hd['gamma']), float(hd['e']),
                                   float(hd['es']), float(hd['t']), float(
                                       hd['r1']), float(hd['betaP']),
                                   float(hd['betaK']), float(hd['betaL']), float(
                                       hd['s']), float(hd['l1']),
                                   float(hd['l2']), float(hd['rL']), float(hd['r2L']), float(hd['r2']))

        gates_dist = hill_profile.es / (hill_profile.gates-1)

        return Hill(hd['name'], float(hd['w']), float(hd['w']) + float(hd['l2']), float(hd['gate']), gates_dist, float(hd['headwind']), float(hd['tailwind']), hill_profile)

    def get_jumpers(self):
        jumpers = []
        for jmp in self.jumpers_data:
            jumper = Jumper(jmp['name'], jmp['country'], int(jmp['inrun']),
                            int(jmp['takeoff']), int(jmp['flight']), int(jmp['style']))
            jumpers.append(jumper)
        return jumpers

    def run_competition(self):
        competition_data = self.competitions_data[0]
        seed = int(competition_data['seed'])
        jumpers = self.get_jumpers()
        hill_data = self.get_hill_data_by_name(competition_data['hillname'])
        hill = self.get_hill_from_hill_data(hill_data)
        return CompetitionManager(hill, competition_data, jumpers)

    def present_results(self):
        pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--verbose', action='store_true')
    args = parser.parse_args()
    xd = IOSkiJump('jumpers.csv', 'hills.csv', 'competitions.csv')
    xdd = xd.run_competition()
    xdd.run_competition(debug=args.verbose)
    xdd.present_results()

